from django.urls import path
from users import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

app_name = 'user'

urlpatterns = [
    # 회원가입
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    
    # 비밀번호 변경
    path('info/pw/<int:user_id>/', views.ChangePasswordView.as_view(), name='change_pw_view'),

    # 로그인
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 이메일 인증
    path('activate/<uidb64>/<token>/', views.UserActivate.as_view(), name='activate'),

    # 마이 페이지
    path('mypage/<int:user_id>/', views.MyPageView.as_view(), name='my_page_view'),
]
