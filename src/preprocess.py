import pandas as pd 
import ast
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def convert(obj):
    L = []

    for i in ast.literal_eval(obj):
        L.append(i['name'])

    return L

def fetch_director(obj):
    L = []

    for i in ast.literal_eval(obj):

        if i['job'] == 'Director':
            L.append(i['name'])
            break

    return L

def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

def preprocess_data(movies_path, credits_path):

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # Merge dataset 
    movies = movies.merge(credits, on="title")

    # select useful columns 
    movies = movies[
        ['movie_id',
         'title',
         'overview',
         'genres',
         'keywords',
         'cast',
         'crew']
    ]

    # removing missing values 
    movies.dropna(inplace=True)

    # convert JSON string to list 
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    # take top 3 cast members 
    movies['cast'] = movies['cast'].apply(lambda x: convert(x)[:3])

    # Get director 
    movies['crew'] = movies['crew'].apply(fetch_director)

    # Split overview text 
    movies['overview'] = movies['overview'].apply(lambda x : x.split())

    # Remove Spaces 
    for feature in ['genres', 'keywords', 'cast', 'crew']:

        movies[feature] = movies[feature].apply(
            lambda x: [i.replace(" ", "") for i in x]
        )

    # Create tags 
    movies['tags'] = (
        movies['overview']
        + movies['genres']
        + movies['keywords']
        + movies['cast']
        + movies['crew']
    )

    new_df = movies[['movie_id','title', 'tags']]

    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

    # Apply stemming 
    new_df['tags'] = new_df['tags'].apply(stem)

    return new_df


