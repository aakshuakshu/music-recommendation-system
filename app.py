import streamlit as st

st.title("🎵 Intelligent Music Recommendation System")

genres = st.multiselect(
    "Select Your Favorite Genres:",
    ["Hip-Hop", "Pop", "Classical", "Rock", "Jazz", "EDM"]
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
    st.success("Generating recommendations based on your preferences...")
