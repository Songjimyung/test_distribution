from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class UserSigninTest(APITestCase):
    def setUp(self):
        self.data = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
        }
        self.user = User.objects.create_user('test1234', 'test@testuser.com', 'Qwerasdf1234!')

    def test_signin(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)


class UserMypageTest(APITestCase):
    def setUp(self):
        self.data = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
        }
        self.user = User.objects.create_user('test1234', 'test@testuser.com', 'Qwerasdf1234!')

    def test_signin(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(
            path=reverse("my_page_view", args=['1']),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_name'], self.data['user_name'])
