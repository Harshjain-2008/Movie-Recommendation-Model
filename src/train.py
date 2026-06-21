import joblib

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from preprocess import preprocess_data

def train():

    movies = preprocess_data("data/movies.csv","data/credits.csv")

    cv = CountVectorizer(max_features=5000,stop_words='english')

    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    # save model files 

    joblib.dump(movies,"models/movies_list.pkl")
    joblib.dump(similarity,"models/similarity.pkl")

    print("Training complete successfully ")

if __name__ == "__main__":
    train()
    
       


