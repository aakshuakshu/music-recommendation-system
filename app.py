import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------------
# 1. Load Dataset
# -------------------------
df = pd.read_csv('songs_dataset.csv')

# -------------------------
# 2. App Title & Description
# -------------------------
st.set_page_config(page_title="🎵 Intelligent Music Recommender", layout="wide")
st.title("🎵 Intelligent Music Recommendation System")
st.subheader("MCA Final Year Project - ML-Based Recommendation")
st.write("Select a song you like, and get smart recommendations!")

# -------------------------
# 3. Song Selection
# -------------------------
song_options = df['song_name'].unique()
selected_song = st.selectbox("Select a Song", song_options)

# Show album art for selected song
song_info = df[df['song_name'] == selected_song].iloc[0]
st.image(song_info['image_url'], width=200)
st.write(f"**Artist:** {song_info['artist']}  |  **Album:** {song_info['album']}")
st.write(f"**Genre:** {song_info['genre']}  |  **Mood:** {song_info['mood']}")

# -------------------------
# 4. Recommendation Calculation
# -------------------------
feature_cols = ['energy', 'danceability', 'tempo']
song_features = df[feature_cols]

# Compute similarity
similarity_matrix = cosine_similarity(song_features)
song_index = df[df['song_name'] == selected_song].index[0]
similar_songs_idx = np.argsort(similarity_matrix[song_index])[::-1]

# -------------------------
# 5. Display Recommended Songs
# -------------------------
st.subheader("🎧 Recommended Songs:")

# Top 5 recommendations
top_n = 5
rec_idx = [i for i in similar_songs_idx if i != song_index][:top_n]

# Display in cards using columns
cols = st.columns(top_n)
for i, idx in enumerate(rec_idx):
    with cols[i]:
        rec_song = df.iloc[idx]
        st.image(rec_song['image_url'], width=150)
        st.write(f"**{rec_song['song_name']}**")
        st.write(f"*{rec_song['artist']}*")
        st.write(f"Genre: {rec_song['genre']}")
        st.write(f"Mood: {rec_song['mood']}")
