from django.urls import path
from movies import views

urlpatterns = [
    path('detail/', views.MovieListView.as_view(), name='detail'),
]