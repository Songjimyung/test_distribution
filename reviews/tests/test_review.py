from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from faker import Faker


class ReviewCreateTest(APITestCase):
    '''
    Review가 잘 작성되는지 검증하는 Test class입니다.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "user_name":"leedddd",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!"
        }
        cls.review_data = {'content':'모성의 목소리 조차 박탈한 뒤 그 크신 사랑만을 돌림노래로 부르는 공업적 최루법.'}
        cls.user = User.objects.create_user('leedddd', 'test@testuser.com', 'Qwerasdf1234!')

    # .client부분이 classmethod가 아니기 때문에 cls.client.post ..은 에러가 나서 따로 setUp으로
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # access_token등의 헤더가 없어서 실패해야 하는 테스트
    def test_fail_if_not_logged_in(self):
        url = reverse("review_view")
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, 401)

    def test_create_review(self):
        response = self.client.post(
            path = reverse("review_view"),
            data = self.review_data,
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)


class ReviewReadTest(APITestCase):
    '''
    Review가 잘 불려오는지 검증하는 Test class입니다.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.reviews=[]
        for _ in range(10):
            cls.faker = Faker()
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
            first_name = cls.faker.first_name()
            last_name = cls.faker.last_name()
            company = cls.faker.company().split()[0].strip(',')
            dns_org = cls.faker.random_choices(
                elements=list_of_domains,
                length=1
            )[0]
            email_faker = f"{first_name}.{last_name}@{company}.{dns_org}".lower()
            cls.user = User.objects.create_user(cls.faker.name()+"A1!", email_faker, cls.faker.word()+"B2@")
            cls.reviews.append(Review.objects.create(content=cls.faker.sentence(), user=cls.user))

    def test_get_review(self):
        for i, review in enumerate(self.reviews):
            url = reverse("review_view")
            response = self.client.get(url)
            serializer = ReviewSerializer(review).data
            for key, value in serializer.items():
                self.assertEqual(response.data[i][key], value)


class ReviewDetailTest(APITestCase):
    '''
    Review가 잘 수정되는지 검증하는 Test class입니다.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "user_name":"leedddd",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!"
        }
        cls.review_data = {'content':'모성의 목소리 조차 박탈한 뒤 그 크신 사랑만을 돌림노래로 부르는 공업적 최루법.'}
        cls.review_data_new = {'content':'전편보다 낫다는 이야기를 듣고 보았다. 그렇긴 했다.'}
        cls.user = User.objects.create_user('leedddd', 'test@testuser.com', 'Qwerasdf1234!')

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    def test_put_review(self):
        # 리뷰 생성 후
        response = self.client.post(
            path=reverse("review_view"),
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