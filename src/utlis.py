import requests

API_KEY = "31857e8a7605df7e505c6eb366287764"

def fetch_movie_details(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}?api_key={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    poster_path = data.get("poster_path")

    poster = None

    if poster_path:
         poster = (
            "https://image.tmdb.org/t/p/w500/"
            + poster_path
        )
         
    rating = data.get('vote_average')

    genres = ", ".join(
        [g['name'] for g in data.get('genres', [])]
    )

    return poster,rating,genres     
