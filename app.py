import joblib
import streamlit as st
import os

if not os.path.exists("models/movie_list.pkl"):
    from src.train import train
    train()

from src.recommender import recommend
from src.utlis import fetch_movie_details

# Page Configuration 
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

# load trained movies list 
movies = joblib.load("models/movies_list.pkl")

# Sidebar 
with st.sidebar:
    st.title("About")
    st.write("""
     Movie Recommendation System

    Algorithm Used
    - Content-Based Filtering
    - Cosine Similarity

    Features:
    - Movie Search
    - Smart Recommendations
    - Posters
    - Ratings
    - Genres

    Developed by Harsh Jain
    """)
    
    st.metric("Movies in Dataset", len(movies))

# Main Title 
st.title("Movie Recommendation System")
st.markdown("Discover Movies similar to your Favrouties")

# Search box 
search_query = st.text_input("Search for Movie")

selected_movie = None

if search_query:

    suggestion = movies[
        movies['title'].str.contains(
            search_query,
            case=False,
            na=False
        )
    ]['title'].head(10).tolist()

    if suggestion:
        selected_movie = st.selectbox(
            "select a movie",
            suggestion
        )

    else:
        st.warning("No movie found")

# Recommendation button 
if st.button("Recommend Movies"):

    if selected_movie:
        recommendations = recommend(selected_movie)

        st.subheader("Recommended Movies")

        cols = st.columns(5)


        for col, movie in zip(cols, recommendations):
            poster, rating, genres = fetch_movie_details(
                movie['movie_id']
            )

            with col:
                if poster:
                    st.image(poster)

                st.markdown(f" {movie['title']}")
                st.write(f"⭐ Rating: {rating}")
                st.caption(f"🎭 {genres}")
    else:
        st.warning("Please search and select a movie")

# footer 
st.markdown("---")
st.markdown(
    "<center>Made by Harsh Jain</center>",
    unsafe_allow_html=True
)



