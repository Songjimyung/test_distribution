from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from movies.models import Movie, Genre


class ReviewLikeTest(APITestCase):
    '''
    Review의 좋아요 기능이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.

    테스트 데이터는 `setUpTestData` 메서드를 사용하여 테스트 사용자와 리뷰 데이터를 설정합니다.

    Review Model의 `get_absolute_url` 메서드를 통해 <int:review_id>/ 값이 변경되더라도
    리뷰가 올바르게 수정 및 삭제되는지 확인합니다.
    like method의 review_id부분을 우선은 1로 처리해놓았습니다. 추후 수정예정
    '''
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "user_name": "leedddd",
            "email": "test@testuser.com",
            "password": "Qwerasdf1234!"
        }
        cls.movie_data = {
            "id": "397567",
            "title": "신과함께-죄와 벌",
            "release_date": "2017-12-20",
            "overview": "살인, 나태, 거짓, 불의, 배신, 폭력, 천륜 7개의 지옥에서 7번의 재판을 무사히 통과한 망자만이 환생하여\
                새로운 삶을 시작할 수 있다. 화재 사고 현장에서 여자아이를 구하고 죽음을 맞이한 소방관 자홍, 그의 앞에 저승차사\
                해원맥과 덕춘이 나타난다. 자신의 죽음이 아직 믿기지도 않는데 덕춘은 정의로운 망자이자 귀인이라며 그를 치켜세운다.",
            "vote_average": "7.9",
            "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/5j2YVF7VouLG0Ze96SEsj4DnVQM.jpg",
            "genres": ["액션", "모험", "판타지", "스릴러"]
        }
        # ForeignKey로 연결될 Movie Data를 생성합니다.
        cls.movie = Movie.objects.create(
            id=cls.movie_data['id'],
            title=cls.movie_data['title'],
            release_date=cls.movie_data['release_date'],
            overview=cls.movie_data['overview'],
            vote_average=cls.movie_data['vote_average'],
            poster_path=cls.movie_data['poster_path']
        )
        # Movie와 Genre가 ManyToMany관계라서 .set() 메소드로 설정합니다.
        cls.movie.genres.set(Genre.objects.filter(name__in=cls.movie_data['genres']))
        cls.review_data = {'id': 1,'content': '모성의 목소리 조차 박탈한 뒤 그 크신 사랑만을 돌림노래로 부르는 공업적 최루법.', 'rating': '2'}
        cls.user = User.objects.create_user('leedddd', 'test@testuser.com', 'Qwerasdf1234!')

    def setUp(self):
        # 'token_obtain_pair' 엔드포인트를 호출하여 액세스 토큰을 얻습니다.
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_data).data['access']

    def test_like_review(self):
        '''
        - 리뷰 좋아요:
            1. 새로운 리뷰를 생성합니다.
            2. 주어진 내용을 사용하여 리뷰 객체를 가져옵니다.
            3. like_url로 post요청을 보냅니다.
            4. status_code가 200인지 확인하여 좋아요가 성공적으로 이루어졌는지 확인합니다.
        '''
        # 리뷰 생성
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)

        # 리뷰 좋아요 테스트
        like_url = reverse("review_like_view", kwargs={"movie_id": self.movie.id, "review_id": 1})
        response = self.client.post(
            path=like_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], '좋아요 성공!')

    def test_unlike_review(self):
        '''
        - 리뷰 좋아요 취소:
            1. 새로운 리뷰를 생성합니다.
            2. 주어진 내용을 사용하여 리뷰 객체를 가져옵니다.
            3. like_url로 post요청을 보냅니다.
            4. status_code가 200인지 확인하여 좋아요가 성공적으로 이루어졌는지 확인합니다.
            3. like_url로 post요청을 보냅니다.
            3. status_code가 200인지 확인하여 좋아요가 성공적으로 취소되었는지 확인합니다.
        '''
        # 리뷰 생성
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)

        # 리뷰 좋아요 테스트
        like_url = reverse("review_like_view", kwargs={"movie_id": self.movie.id, "review_id": 1})
        response = self.client.post(
            path=like_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], '좋아요 성공!')

        # 리뷰 좋아요 취소 테스트
        like_url = reverse("review_like_view", kwargs={"movie_id": self.movie.id, "review_id": 1})
        response = self.client.post(
            path=like_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], '좋아요 취소!')