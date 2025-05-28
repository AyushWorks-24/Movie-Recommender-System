import streamlit as st
import pickle
import pandas as pd

# TMDb image URL prefix
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_data = movies.iloc[i[0]]
        recommended_titles.append(movie_data.title)
        poster_path = movie_data.get("poster_path", None)
        if poster_path:
            recommended_posters.append(f"{IMAGE_BASE_URL}{poster_path}")
        else:
            recommended_posters.append("https://via.placeholder.com/200x300?text=No+Image")

    return recommended_titles, recommended_posters


# Page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Body font and background */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #fafafa;
    }

    /* Title style */
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }

    /* Recommend button styling */
    div.stButton > button:first-child {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-weight: 600;
        border: 2px solid #000000 !important;
        border-radius: 10px;
        height: 2.7em;
        width: 130px;
        font-size: 16px;
        transition: background-color 0.3s ease, color 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    div.stButton > button:first-child:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
        cursor: pointer;
        border: 2px solid #000000 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Movie card styling */
    .movie-card {
        background-color: #f0f4f8;
        padding: 15px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
        margin-bottom: 20px;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.12);
    }
    .movie-poster {
        width: 100%;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .movie-title {
        font-weight: 700;
        font-size: 18px;
        color: #2c3e50;
        margin: 0;
        user-select: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    titles, posters = recommend(selected_movie_name)

    st.markdown("<h3 style='color:#FF6347; margin-bottom:25px;'>🎥 Recommended Movies</h3>", unsafe_allow_html=True)
    cols = st.columns(len(titles))

    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{posters[idx]}" alt="{titles[idx]}" class="movie-poster" />
                    <p class="movie-title">{titles[idx]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
