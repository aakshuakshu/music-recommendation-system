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

    df = pd.read_csv("dataset.csv")

    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    # =============================
    # 1️⃣ Build User Taste Vector
    # =============================

    if genres:
        user_df = df[df["genre"].isin(genres)]
    else:
        user_df = df.copy()

    if user_df.empty:
        st.warning("No songs found for selected genre.")
        st.stop()

    user_vector = user_df[feature_cols].mean().values.reshape(1, -1)

    # Add mood_score
    mood_score = user_df["valence"].mean()
    user_vector[0][feature_cols.index("valence")] = mood_score

    # =============================
    # 2️⃣ Context Weighting
    # =============================

    weights = np.ones(len(feature_cols))

    if mood == "Happy":
        weights[feature_cols.index("valence")] *= 1.5
    elif mood == "Sad":
        weights[feature_cols.index("valence")] *= 0.7

    if activity == "Party":
        weights[feature_cols.index("energy")] *= 1.5
        weights[feature_cols.index("danceability")] *= 1.5
    elif activity == "Relax":
        weights[feature_cols.index("energy")] *= 0.7

    weighted_features = df[feature_cols] * weights

    # =============================
    # 3️⃣ Content Similarity
    # =============================

    similarity_scores = cosine_similarity(
        user_vector,
        weighted_features
    )

    df["content_score"] = similarity_scores.flatten()

    # =============================
    # 4️⃣ Collaborative Score (Simple Popularity Proxy)
    # =============================

    if "popularity" in df.columns:
        df["collab_score"] = df["popularity"] / df["popularity"].max()
    else:
        df["collab_score"] = 0.5

    # =============================
    # 5️⃣ Final Score Formula
    # =============================

    df["final_score"] = (
        0.4 * df["content_score"] +
        0.4 * df["collab_score"] +
        0.2 * df["content_score"]  # context already applied in weighting
    )

    recommendations = df.sort_values(
        by="final_score",
        ascending=False
    ).head(10)

    st.success("Top 10 Recommended Songs")

    st.dataframe(
        recommendations[[
            "track_name",
            "artists",
            "album_name"
        ]]
    )

