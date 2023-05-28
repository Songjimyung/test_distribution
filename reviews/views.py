from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from reviews.models import Review
from movies.models import Movie
from reviews.serializers import ReviewSerializer, ReviewCreateSerializer


# 후기 목록과 작성
class ReviewView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # 모든 후기 불러오기
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 후기 작성하기
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 후기 상세페이지 수정, 삭제    
class ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # 후기 수정하기
    def put(self, request, movie_id, review_id):
        review = get_object_or_404(Review, id = review_id, movie=movie_id)
        # 본인이 작성한 후기이 맞다면
        if request.user == review.user:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 본인의 후기이 아니라면
        else:
            return Response({'message':'해당 리뷰를 수정할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    # 후기 삭제하기
    def delete(self, request, movie_id, review_id):
        review = get_object_or_404(Review, id = review_id, movie=movie_id)
        # 본인이 작성한 후기이 맞다면
        if request.user == review.user:
            review.delete()
            return Response({'message':'후기가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        # 본인의 후기이 아니라면
        else:
            return Response({'message':'해당 리뷰를 삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def post(self, request, movie_id, review_id):
        review = get_object_or_404(Review, id = review_id, movie=movie_id)
        if request.user in review.like.all():
            review.like.remove(request.user)
            return Response({'message':'좋아요 취소!'}, status=status.HTTP_200_OK)
        else:
            review.like.add(request.user)
            return Response({'message':'좋아요 성공!'}, status=status.HTTP_200_OK)
