from django.shortcuts import render
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import MovieSerializer
from rest_framework.views import APIView
import requests
import random

# Create your views here.

class MovieListView(APIView):
    def get(self, request):
        genres_url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {
                    "api_key": "dfffda402827c71395fe46139633c254",
                    "language": "ko-KR"
                 }

        response = requests.get(genres_url, params=params)
        genres_data = response.json()

        # 장르 정보 Genre 모델에 저장
        genres = genres_data['genres']
        for genre in genres:
            Genre.objects.get_or_create(id=genre['id'], defaults={'name': genre['name']})

        # 영화 정보 가져오기
        movies_url = "https://api.themoviedb.org/3/movie/popular"
        params = {
                    "api_key": "dfffda402827c71395fe46139633c254",
                    "language": "ko-KR"
                 }

        response = requests.get(movies_url, params=params)
        movies_data = response.json()['results']
        
        random_movies = random.sample(movies_data, 10)
        
        serialized_data = []

        # 영화 정보 저장
        for movie_data in random_movies:
            genre_ids = movie_data['genre_ids']
            genres = Genre.objects.filter(id__in=genre_ids)
            genre_names = [genre.name for genre in genres]
            poster_path = "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
            movie = Movie(
                id=movie_data['id'],
                title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                vote_average=movie_data['vote_average'],
                poster_path=poster_path
            )
            movie.save()
            movie.genres.set(genres)
            # 영화 정보 출력
            movie_data['genre_ids'] = genre_names
            movie_data['poster_path']=poster_path
            movie_json = {
                "id": movie_data['id'],
                "title": movie_data['title'],
                "overview": movie_data['overview'],
                "release_date" : movie_data['release_date'],
                "vote_average" : movie_data['vote_average'],
                "genres" : movie_data['genre_ids'],
                "poster_path" : movie_data['poster_path']
            }
            
            serialized_data.append(movie_json)
            
        return Response(serialized_data)
          
