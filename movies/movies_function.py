import csv
import requests
 
def save_movies_to_csv(file_path):
    movies_url = "https://api.themoviedb.org/3/movie/popular"
    genres_url = "https://api.themoviedb.org/3/genre/movie/list"
    selected_fields = ["title", "overview", "release_date", "vote_average", "poster_path", "genre_ids"]
    
    params = {
        "api_key": "dfffda402827c71395fe46139633c254",
        "language": "ko-KR"
    }
    #기존에 있던 데이터
    existing_data = []
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            existing_data = list(reader)
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
    for page in range(1, 201):
        params["page"] = page

        response = requests.get(movies_url, params=params)
        if response.status_code == 200:
            movies_data = response.json().get('results', [])

            for item in movies_data:
                selected_data = {field: item.get(field) for field in selected_fields}
                
                genre_ids = selected_data.get('genre_ids', [])
                genre_names = [genre_mapping.get(genre_id) for genre_id in genre_ids]
                #장르 ID에서 이름으로 변환
                selected_data['genre_ids'] = genre_names
                
                is_duplicate = False
                for data in existing_data:
                    if selected_data == data:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    new_movies.append(selected_data)
        else:
            print(f"Failed to retrieve movie data for page {page}")

    if new_movies:
        with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=selected_fields)
            if csv_file.tell() == 0:
                writer.writeheader()
            writer.writerows(new_movies)

    print("Movies saved to CSV file successfully.")
        # csv_filename = "movie_data.csv"
        # existing_data = []
        # with open(csv_filename, "r", newline="", encoding="utf-8") as csv_file:
        #     reader = csv.DictReader(csv_file)
        #     existing_data = list(reader)
        #     selected_fields = ["title", "overview", "release_date", "vote_average", "poster_path", "genres"]

        # for item in movies_data:
        #     selected_data = {field: item[field] for field in selected_fields}
            
        #     is_duplicate = False
        #     for data in existing_data:
        #         if selected_data == data:
        #             is_duplicate = True
        #             break
        #     if not is_duplicate:
        #         existing_data.append(selected_data)
        # fieldnames = selected_fields    
        # with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerows(existing_data)