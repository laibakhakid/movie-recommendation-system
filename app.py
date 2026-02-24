import streamlit as st
import pickle
import requests

# --- Fetch poster from TMDb safely ---
import os

def fetch_poster(movie_id):
    try:
        api_key = os.getenv("TMDB_API_KEY")
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
        )
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

# --- Load data ---
movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# --- Recommendation function ---
def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

# --- Streamlit UI ---
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <div style='background-color:#4B0082;padding:20px;border-radius:10px 10px 0 0;'>
        <h1 style='text-align:center;color:white;margin:0;font-family:Arial, sans-serif;'>🎬 Movie Recommendation System</h1>
        <p style='text-align:center;color:white;margin:0;font-family:Arial, sans-serif;'>Find the best movies similar to your favorite ones!</p>
    </div>
""", unsafe_allow_html=True)

st.write("")  # spacing

# --- Movie Selection ---
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies_df['title'].values
)

# --- Recommendation ---
if st.button("Recommend 🎯"):
    names, posters = recommend(selected_movie_name)
    
    st.subheader("Recommended Movies:")
    
    # Create 5 columns for 5 recommendations
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        # Big, attractive, centered title using HTML
        col.markdown(
            f"<h3 style='text-align: center; color: #4B0082; font-family: Arial, sans-serif;'>{names[idx]}</h3>",
            unsafe_allow_html=True
        )
        # Poster with fixed width
        col.image(posters[idx], width=200)

