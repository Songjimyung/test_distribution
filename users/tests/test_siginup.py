from django.urls import reverse
from rest_framework.test import APITestCase


class UserSignupTest(APITestCase):
    def test_signup(self):
        url = reverse("sign_up")
        user_data = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
            "re_password":"Qwerasdf1234!"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)

    def test_signup_sameid(self):
        url = reverse("sign_up")
        user_data1 = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
            "re_password":"Qwerasdf1234!"
        }
        response = self.client.post(url, user_data1)
        self.assertEqual(response.status_code, 201)

        user_data2 = {
            "user_name":"test1234",
            "email":"email@testuser.com",
            "password":"Asdfzxcv1234!",
            "re_password":"Asdfzxcv1234!"
        }
        response = self.client.post(url, user_data2)
        self.assertEqual(response.status_code, 400)

    def test_signup_sameemail(self):
        url = reverse("sign_up")
        user_data1 = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
            "re_password":"Qwerasdf1234!"
        }
        response = self.client.post(url, user_data1)
        self.assertEqual(response.status_code, 201)

        user_data2 = {
            "user_name":"diff1234",
            "email":"test@testuser.com",
            "password":"Asdfzxcv1234!",
            "re_password":"Asdfzxcv1234!"
        }
        response = self.client.post(url, user_data2)
        self.assertEqual(response.status_code, 400)
