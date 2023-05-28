from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class UserSignupTest(APITestCase):
    '''
    회원가입이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.
    '''
    def test_signup(self):
        '''
        - 회원가입:
            1. 사용자 데이터를 생성합니다.
            2. 생성된 사용자 데이터로 POST 요청을 보냅니다.
            3. status_code 201인지 확인하여 회원가입이 성공적으로 이루어졌는지 확인합니다.
        '''
        url = reverse("user:sign_up")
        user_data = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
            "re_password":"Qwerasdf1234!"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().user_name, 'test1234')

    def test_signup_sameid(self):
        '''
        - 동일한 사용자 ID로 회원가입하는 경우:
            1. 첫 번째 사용자 데이터를 생성하여 POST 요청을 보냅니다.
            2. status_code 201인지 확인하여 회원가입이 성공적으로 이루어졌는지 확인합니다.
            3. 동일한 사용자 ID를 가진 두 번째 사용자 데이터를 생성하여 POST 요청을 보냅니다.
            4. status_code 400인지 확인하여 회원가입이 실패하는지 확인합니다.
        '''
        url = reverse("user:sign_up")
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
        '''
        - 동일한 이메일로 회원가입하는 경우:
            1. 첫 번째 사용자 데이터를 생성하여 POST 요청을 보냅니다.
            2. status_code 201인지 확인하여 회원가입이 성공적으로 이루어졌는지 확인합니다.
            3. 다른 사용자 ID를 가진 두 번째 사용자 데이터를 생성하여 POST 요청을 보냅니다.
            4. status_code 400인지 확인하여 회원가입이 실패하는지 확인합니다.
        '''
        url = reverse("user:sign_up")
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
