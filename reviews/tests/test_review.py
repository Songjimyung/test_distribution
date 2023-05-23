from django.test.client import encode_multipart, RequestFactory
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from faker import Faker


class ReviewCreateTest(APITestCase):
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
        response = self.client.post(url, self.review_data) # 에러나는부분
        self.assertEqual(response.status_code, 401)

    def test_create_review(self):
        response = self.client.post(
            path = reverse("review_view"),
            data = self.review_data,
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 201)


class ReviewReadTest(APITestCase):
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
                print(key,value)
                self.assertEqual(response.data[i][key], value)