from django.urls import path
from reviews import views

urlpatterns = [
    path('', views.ReviewView.as_view(), name='review_view'),
    path('<int:movie_id>/', views.ReviewView.as_view(), name='review_view'),
    path('<int:movie_id>/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:movie_id>/<int:review_id>/like/', views.LikeView.as_view(), name='like_view'),
]
