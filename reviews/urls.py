from django.urls import path
from reviews import views

urlpatterns = [
    path('', views.ReviewView.as_view(), name='review_view'), # <str:title>/ 이거 넣어야할지 Movie 추가되면 생각해보기
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:review_id>/like/', views.LikeView.as_view(), name='like_view'),
]
