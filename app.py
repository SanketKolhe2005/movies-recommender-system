import os
import streamlit as st
import pickle

if not os.path.exists("similarity.pkl"):
    st.error("Similarity file not found. This app is for demo only.")
    st.stop()

similarity = pickle.load(open("similarity.pkl", "rb"))

import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- POSTER FUNCTION --------------------
@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a430df470f620e41d343106521575a06&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://dummyimage.com/500x750/000/fff&text=No+Poster"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return "https://dummyimage.com/500x750/000/fff&text=Error"


# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        if len(recommended_movies) == 5:
            break

        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)

        # skip movies with no poster
        if "dummyimage" in poster:
            continue

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters


# -------------------- LOAD DATA --------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# -------------------- STREAMLIT UI --------------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].tolist()
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0], width=200)

    with col2:
        st.text(names[1])
        st.image(posters[1], width=200)

    with col3:
        st.text(names[2])
        st.image(posters[2], width=200)

    with col4:
        st.text(names[3])
        st.image(posters[3], width=200)

    with col5:
        st.text(names[4])
        st.image(posters[4], width=200)
