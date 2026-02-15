import streamlit as st
import pandas as pd
from utils import load_and_clean_data
from recommender import generate_recommendations

st.set_page_config(page_title="Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")

# Load data
df = load_and_clean_data("dataset.csv")

# Layout
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("🎧 Your Preferences")

    genres = st.multiselect(
        "Select Genre",
        sorted(df["genre"].unique())
    )

    mood = st.selectbox(
        "Select Mood",
        ["Happy", "Sad", "Chill", "Energetic"]
    )

    activity = st.selectbox(
        "Select Activity",
        ["Party", "Gym", "Study", "Relax"]
    )

    liked_songs = st.text_area(
        "Previously Liked Songs"
    )

    generate = st.button("Generate Recommendations")

if generate:

    if not liked_songs.strip():
        st.info("No listening history found. Using genre and context-based filtering.")

    recommendations = generate_recommendations(
        df, genres, mood, activity
    )

    if recommendations is None:
        st.warning("No songs found for selected genre.")
    else:
        with right_col:
            st.header("🎵 Top Recommendations")

            recommendations["confidence"] = (
                recommendations["final_score"] * 100
            ).round(2)

            st.dataframe(
                recommendations[[
                    "track_name",
                    "artists",
                    "genre",
                    "confidence"
                ]]
            )

        st.subheader("🔎 Why These Songs?")
        st.markdown(f"""
        Based on your love for **{', '.join(genres) if genres else 'various genres'}**,
        your **{mood} mood**, and **{activity} activity**,
        we prioritized high-energy and high-valence tracks.
        """)
