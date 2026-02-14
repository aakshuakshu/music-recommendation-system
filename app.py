import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Music Recommendation System")

st.title("🎵 Intelligent Music Recommendation System")
st.write("MCA Final Year Project - ML Based Recommendation")

# Load dataset
df = pd.read_csv("dataset.csv")

# Drop missing values
df = df.dropna()

# Select important numerical features
features = ['danceability', 'energy', 'loudness', 'tempo']

# Make sure features exist
df = df[features + ['track_name']]

X = df[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Compute similarity
similarity = cosine_similarity(X_scaled)

# Song selection dropdown
song_list = df['track_name'].values
selected_song = st.selectbox("Select a Song", song_list)

def recommend(song):
    index = df[df['track_name'] == song].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_songs = []
    for i in distances:
        recommended_songs.append(df.iloc[i[0]]['track_name'])
    return recommended_songs

if st.button("Recommend"):
    recommendations = recommend(selected_song)
    st.subheader("🎧 Recommended Songs:")
    for song in recommendations:
        st.write(song)
