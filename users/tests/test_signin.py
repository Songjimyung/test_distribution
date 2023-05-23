from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class UserSigninTest(APITestCase):
    '''
    로그인이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.

    테스트 시나리오:
    - 로그인:
        1. User 데이터를 생성합니다.
        2. 생성된 사용자 데이터로 POST 요청을 보냅니다.
        3. status_code가 200인지 확인하여 로그인이 성공적으로 이루어졌는지 확인합니다.
    '''
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
    '''
    마이페이지 GET 요청이 올바르게 이루어지는지 검증하는 테스트 클래스입니다.

    테스트 시나리오:
    - 로그인:
        1. User 데이터를 생성합니다.
        2. 생성된 사용자 데이터로 POST 요청을 보냅니다.
        3. status_code가 200인지 확인하여 로그인이 성공적으로 이루어졌는지 확인합니다.

    - 마이페이지 GET 요청:
        1. 액세스 토큰을 가져옵니다.
        2. 마이페이지 URL을 생성합니다.
        3. GET 요청을 보내고 status_code가 200인지 확인합니다.
        4. response 데이터의 'user_name'이 예상되는 값과 일치하는지 확인합니다.
    '''
    def setUp(self):
        self.data = {
            "user_name":"test1234",
            "email":"test@testuser.com",
            "password":"Qwerasdf1234!",
        }
        self.user = User.objects.create_user('test1234', 'test@testuser.com', 'Qwerasdf1234!')

    def test_signin(self):
        # 'token_obtain_pair' 엔드포인트를 호출하여 액세스 토큰을 얻습니다.
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
