import csv, requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def save_movies_to_csv(file_path):
    movies_url = "https://api.themoviedb.org/3/movie/popular"
    genres_url = "https://api.themoviedb.org/3/genre/movie/list"
    selected_fields = ["id","title", "overview", "release_date", "vote_average", "poster_path", "genre_ids"]
    
    params = {
        "api_key": "dfffda402827c71395fe46139633c254",
        "language": "ko-KR"
    }
    #기존에 있던 데이터
    existing_data = set()
    
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # existing_data에 추가되는 id값과 나중에 비교할 값이 문자열과 정수라 비교 안되던 것. 정수로 바꿔서 저장.
                existing_data.add(int(row['id']))
    except FileNotFoundError:
        pass
    
    #장르 바꿔주기위한 매핑
    genre_mapping = {}
    response = requests.get(genres_url, params=params)
    if response.status_code == 200:
        genres_data = response.json().get('genres')
        #장르 딕셔너리화
        genre_mapping = {genre['id']: genre['name'] for genre in genres_data}
        
    new_movies = []
    for page in range(1,201):
        params["page"] = page

        response = requests.get(movies_url, params=params)
        if response.status_code == 200:
            movies_data = response.json().get('results', [])

            for item in movies_data:
                selected_data = {field: item.get(field) for field in selected_fields}
                
                genre_ids = selected_data.get('genre_ids', [])
                #장르 ID에서 이름으로 변환
                genre_names = [genre_mapping.get(genre_id) for genre_id in genre_ids]
                selected_data['genre_ids'] = genre_names
                # 중복 확인 
                if selected_data['id'] not in existing_data:
                    new_movies.append(selected_data)                    

        else:
            pass

    if new_movies:
        with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=selected_fields)
            for movie in new_movies:
                if movie['id'] not in existing_data:
                    writer.writerow(movie)
            #csv 파일이 비었을 때만 헤더(필드명) 추가
            if csv_file.tell() == 0:
                writer.writeheader()
                writer.writerows(new_movies)

    print("csv파일 저장완료.")
