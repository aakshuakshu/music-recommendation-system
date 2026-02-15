import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")

genres = st.multiselect(
    "Select Your Favorite Genres:",
    ["Hip-Hop", "Pop", "Rock", "Classical", "Jazz", "EDM"]
)

mood = st.selectbox(
    "Select Your Current Mood:",
    ["Happy", "Sad", "Chill", "Energetic"]
)

activity = st.selectbox(
    "Select Your Activity:",
    ["Gym", "Study", "Party", "Relax"]
)

liked_songs = st.text_area(
    "Enter Previously Liked Songs (comma separated):"
)

if st.button("Generate Recommendations"):
    st.success("Recommendations Generated Successfully!")
