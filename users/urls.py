from django.urls import path
from users import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    # 회원가입
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),

    # 회원정보 수정
    path('info/<int:user_id>/', views.UserDetailView.as_view(), name='user_view'),
    
    # 비밀번호 변경
    path('info/pw/<int:user_id>/', views.ChangePasswordView.as_view(), name='change_pw_view'),

    # 로그인
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 마이 페이지
    path('mypage/<int:user_id>/', views.MyPageView.as_view(), name='my_page_view'),

    # 팔로우
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
]
