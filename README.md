# 🎬 Movie Recommendation System

**Machine Learning Project 2**

A content-based movie recommendation system built with Python and Streamlit. The system recommends movies similar to a selected movie, using a similarity matrix and cosine similarity. Dynamic movie posters are fetched from the TMDb API.

## 🔹 Features
- Select a movie from the dataset
- Get top 5 similar recommendations instantly
- Dynamic poster retrieval using TMDb API
- Interactive web interface with Streamlit

## 🔹 Tech Stack
- Python
- Streamlit
- Pandas & NumPy
- Scikit-learn (for similarity computation)
- TMDb API integration

## 🔹 Dataset Information
The datasets used in this project **cannot be uploaded to GitHub** due to size/privacy restrictions.  

**Datasets:**
1. `movies.pkl` — Contains movie titles, IDs, and metadata for similarity computation  
2. `similarity.pkl` — Precomputed similarity matrix between movies  

**Source:**  
- Movie data is obtained from [TMDb (The Movie Database)](https://www.themoviedb.org/) API  
- Users need to generate their own dataset or use the provided preprocessing script (if included) to recreate the `.pkl` files.

---

## 🔹 How It Works
1. User selects a movie  
2. Similarity scores are computed across the dataset  
3. Top 5 movies are returned along with posters  
4. Results displayed in a responsive, user-friendly UI

---

## 🔹 Installation
```bash
git clone https://github.com/laibakhakid/movie-recommendation-system.git
cd movie-recommendation-system
pip install -r requirements.txt
streamlit run app.py
