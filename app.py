import streamlit as st

st.title("🎵 Intelligent Music Recommendation System")

# 1. Favorite Genres
genres = st.multiselect(
    "Select Your Favorite Genres:",
    ["Pop", "Rock", "Hip-Hop", "Classical", "Jazz", "EDM"]
)

# 2. Mood Selection
mood = st.selectbox(
    "Select Your Current Mood:",
    ["Happy", "Sad", "Chill", "Energetic"]
)

# 3. Activity Selection
activity = st.selectbox(
    "Select Your Activity:",
    ["Gym", "Study", "Party", "Relax"]
)

# 4. Previously Liked Songs
liked_songs = st.text_area(
    "Enter Previously Liked Songs (comma separated):"
)

# Button
if st.button("Generate Recommendations"):
    st.success("Generating recommendations based on your preferences...")
