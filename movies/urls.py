from django.urls import path
from movies import views

urlpatterns = [
    path('main/', views.MovieListView.as_view(), name='main'),
    path('recommendation/<int:movie_id>/', views.MovieDetailView.as_view(), name='recommendation'),
]