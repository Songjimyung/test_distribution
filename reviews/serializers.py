from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.like.count()

    # Genre가 다음 에러때문에 포함되지 못함. TypeError: Object of type ManyRelatedManager is not JSON serializable
    def get_movie(self, obj):
        return obj.movie.id, obj.movie.title, obj.movie.overview, obj.movie.release_date, obj.movie.vote_average, obj.movie.poster_path
    
    def get_user(self, obj):
        return obj.user.user_name

    class Meta:
        model = Review
        fields = (
            "id",
            "movie",
            "user",
            "content",
            "rating",
            "created_at",
            "updated_at",
            "likes_count",
        )


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("content", "rating",)
