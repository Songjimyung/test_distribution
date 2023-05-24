from django.urls import path
from movies import views

urlpatterns = [
    path('main/', views.MovieListView.as_view(), name='detail'),
    path('recommendation/<int:movie_id>/', views.MovieDetailView.as_view(), name='detail'),
]