import joblib

movies = joblib.load("models/movies_list.pkl")
similarity = joblib.load("models/similarity.pkl")

def recommend(movie):
    index = movies[
        movies['title'] == movie
    ].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse= True,
        key=lambda x: x[1]

    )

    recommended_movies = []

    for i in distances[1:6]:

        movie_data = movies.iloc[i[0]]

        recommended_movies.append({
            'title': movie_data.title,
            'movie_id': movie_data.movie_id
        })

    return recommended_movies    