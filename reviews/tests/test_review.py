from django.urls import reverse
from django.test import Client
from rest_framework.test import APITestCase
from users.models import User
from movies.models import Movie, Genre
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from faker import Faker


class ReviewCreateTest(APITestCase):
    '''
    Review 생성이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.
    `setUpTestData` 메서드를 사용하여 테스트 사용자와 리뷰 데이터를 설정합니다.
    .client부분이 classmethod가 아니기 때문에 cls.client.post ..은 에러가 나서 따로 setUp으로 처리했습니다.
    Movie API가 추가되어 연결했습니다.
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
        cls.review_data = {'content': '모성의 목소리 조차 박탈한 뒤 그 크신 사랑만을 돌림노래로 부르는 공업적 최루법.', 'rating': '2'}
        cls.user = User.objects.create_user('leedddd', 'test@testuser.com', 'Qwerasdf1234!')

    def setUp(self):
        # 'token_obtain_pair' 엔드포인트를 호출하여 액세스 토큰을 얻습니다.
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_data).data['access']

    def test_fail_if_not_logged_in(self):
        '''
        - 로그인하지 않은 경우 실패하는 테스트:
            1. HTTP_AUTHORIZATION에 access토큰을 담지 않은 상태에서 Review 생성 요청을 보냅니다.
            2. status_code가 401인지 확인하여 인증되지 않아 실패하는지 확인합니다.
        '''
        # URL에 movie_id가 항상 달라지므로 kwargs로 넣어줍니다
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, 401)

    def test_create_review(self):
        '''
        - Review 생성:
            1. 인증된 사용자로서 Review 생성 요청을 보냅니다.
            2. status_code가 201인지 확인하여 생성이 성공적으로 이루어졌는지 확인합니다.
        '''
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)


class ReviewReadTest(APITestCase):
    '''
    Review GET 요청이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.

    데이터는 `setUpTestData` 메서드를 사용하여 테스트 사용자와 리뷰 데이터를 설정합니다.
    faker 패키지를 사용하여 10개의 더미 리뷰 데이터를 생성하고, 생성된 10개의 리뷰에 대해
    response와 serializer가 일치하는지 테스트합니다.

    아직 Genre를 고려하지 못했는데 돌아갑니다..

    email_faker 참고코드 : https://gist.github.com/isaqueprofeta/83b8bc9824b55b63012fa975e7264c25
    '''
    @classmethod
    def setUpTestData(cls):
        cls.reviews=[]
        list_of_domains = (
            'com',
            'com.br',
            'net',
            'net.br',
            'org',
            'org.br',
            'gov',
            'gov.br'
        )
        cls.faker = Faker()
        first_name = cls.faker.first_name()
        last_name = cls.faker.last_name()
        company = cls.faker.company().split()[0].strip(',')
        dns_org = cls.faker.random_choices(
            elements=list_of_domains,
            length=1
        )[0]
        email_faker = f"{first_name}.{last_name}@{company}.{dns_org}".lower()
        cls.user = User.objects.create_user(cls.faker.name()+"A1!", email_faker, cls.faker.word()+"B2@")
        for i in range(10):
            cls.client = Client()
            response = cls.client.get('/main/', {
                "api_key": "dfffda402827c71395fe46139633c254",
                "language": "ko-KR"
            })
            cls.movie_data = response.data
            cls.movie_kwargs = {
                'id': cls.movie_data[i]['id'],
                'title': cls.movie_data[i]['title'],
                'release_date': cls.movie_data[i]['release_date'],
                'overview': cls.movie_data[i]['overview'],
                'vote_average': cls.movie_data[i]['vote_average'],
                'poster_path': cls.movie_data[i]['poster_path']
            }
            cls.movie = Movie.objects.get(**cls.movie_kwargs)
            cls.reviews.append(Review.objects.create(content=cls.faker.sentence(), rating=4, movie=cls.movie, user=cls.user))

    def test_get_review(self):
        '''
        - 리뷰 요청:
            1. 10개의 더미 리뷰 데이터를 생성합니다.
            2. 생성된 리뷰 데이터에 대해 GET 요청을 보냅니다.
            3. response와 리뷰 객체의 serializer가 일치하는지 확인합니다.
            (response와 serializer의 각 key - value가 일치하는지 확인합니다.)
        '''
        for i, review in enumerate(self.reviews):
            url = reverse("review_view")
            response = self.client.get(url)
            serializer = ReviewSerializer(review).data
            for key, value in serializer.items():
                self.assertEqual(response.data[i][key], value)


class ReviewDetailTest(APITestCase):
    '''
    Review 수정 및 삭제가 올바르게 이루어지는지 검증하는 테스트 클래스입니다.

    테스트 데이터는 `setUpTestData` 메서드를 사용하여 테스트 사용자와 리뷰 데이터를 설정합니다.

    Review Model의 `get_absolute_url` 메서드를 통해 <int:review_id>/ 값이 변경되더라도
    리뷰가 올바르게 수정 및 삭제되는지 확인합니다.
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
        cls.review_data = {'content': '모성의 목소리 조차 박탈한 뒤 그 크신 사랑만을 돌림노래로 부르는 공업적 최루법.', 'rating': '2'}
        cls.review_data_new = {'content':'전편보다 낫다는 이야기를 듣고 보았다. 그렇긴 했다.', 'rating':'3'}
        cls.user = User.objects.create_user('leedddd', 'test@testuser.com', 'Qwerasdf1234!')

    def setUp(self):
        # 'token_obtain_pair' 엔드포인트를 호출하여 액세스 토큰을 얻습니다.
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_data).data['access']

    def test_put_review(self):
        '''
        - 리뷰 수정:
            1. 새로운 리뷰를 생성합니다.
            2. 주어진 내용을 사용하여 리뷰 객체를 가져옵니다.
            3. `get_absolute_url` 메서드를 호출하여 리뷰 URL을 얻습니다.
            4. 수정된 리뷰 데이터를 포함하여 리뷰 URL로 PUT 요청을 보냅니다.
            5. status_code가 200인지 확인하여 수정이 성공적으로 이루어졌는지 확인합니다.
        '''
        # 리뷰 생성
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)
        review = Review.objects.get(content=self.review_data['content'])  # 리뷰 객체 가져오기
        review_url = review.get_absolute_url() # <int:review_id>/값에 관계없이 url 가져오기

        # 리뷰 수정 테스트
        response = self.client.put(
            path=review_url,
            data=self.review_data_new,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        '''
        - 리뷰 삭제:
            1. 새로운 리뷰를 생성합니다.
            2. 주어진 내용을 사용하여 리뷰 객체를 가져옵니다.
            3. `get_absolute_url` 메서드를 호출하여 리뷰 URL을 얻습니다.
            4. 리뷰 URL로 DELETE 요청을 보냅니다.
            5. status_code가 204인지 확인하여 삭제가 성공적으로 이루어졌는지 확인합니다.
        '''
        # 리뷰 생성
        url = reverse("review_view", kwargs={"movie_id": self.movie.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)
        review = Review.objects.get(content=self.review_data['content'])
        review_url = review.get_absolute_url()

        # 리뷰 삭제 테스트
        response = self.client.delete(
            path=review_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 204)