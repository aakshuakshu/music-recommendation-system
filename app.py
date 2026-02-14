import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------------
# 1. Load Processed Dataset
# -------------------------
try:
    df = pd.read_csv('processed_music_dataset.csv')  # processed CSV
except FileNotFoundError:
    st.error("Processed dataset not found! Make sure 'processed_music_dataset.csv' exists.")
    st.stop()

# -------------------------
# 2. Check Required Columns
# -------------------------
required_cols = [
    'track_name', 'artists', 'album_name', 'track_genre',
    'tempo', 'energy', 'danceability', 'loudness', 'valence', 'popularity'
]

missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    st.error(f"The following required columns are missing in the CSV: {missing_cols}")
    st.stop()

# -------------------------
# 3. App Title & Description
# -------------------------
st.set_page_config(page_title="🎵 Intelligent Music Recommender", layout="wide")
st.title("🎵 Intelligent Music Recommendation System")
st.subheader("MCA Final Year Project - ML-Based Recommendation")
st.write("Select a song you like, and get smart recommendations!")

# -------------------------
# 4. Song Selection
# -------------------------
song_options = df['track_name'].unique()
selected_song = st.selectbox("Select a Song", song_options)

# Display song info
song_info = df[df['track_name'] == selected_song].iloc[0]
st.write(f"**Artist:** {song_info['artists']}  |  **Album:** {song_info['album_name']}")
st.write(f"**Genre:** {song_info['track_genre']}  |  **Popularity:** {song_info['popularity']}")

# -------------------------
# 5. Recommendation Calculation
# -------------------------
feature_cols = ['energy', 'danceability', 'tempo', 'loudness', 'valence']
song_features = df[feature_cols]

# Compute cosine similarity
similarity_matrix = cosine_similarity(song_features)
song_index = df[df['track_name'] == selected_song].index[0]
similar_songs_idx = np.argsort(similarity_matrix[song_index])[::-1]

# -------------------------
# 6. Display Recommended Songs
# -------------------------
st.subheader("🎧 Recommended Songs:")

top_n = 5
rec_idx = [i for i in similar_songs_idx if i != song_index][:top_n]

cols = st.columns(top_n)
for i, idx in enumerate(rec_idx):
    with cols[i]:
        rec_song = df.iloc[idx]
        st.write(f"**{rec_song['track_name']}**")
        st.write(f"*{rec_song['artists']}*")
        st.write(f"Album: {rec_song['album_name']}")
        st.write(f"Genre: {rec_song['track_genre']}")
        st.write(f"Popularity: {rec_song['popularity']}")
