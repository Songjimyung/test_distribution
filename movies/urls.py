from django.urls import path
from movies import views

urlpatterns = [
    path('main/', views.MovieListView.as_view(), name='detail'),
    path('recommendation/<str:movie_title>/', views.MovieDetailView.as_view(), name='detail'),
]