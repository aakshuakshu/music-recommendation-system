import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    df = pd.read_csv("dataset.csv")
    return df


# Remove duplicates
def load_data():
    df = pd.read_csv("dataset.csv")

    df = df.drop_duplicates(subset=["track_name", "artists"])

    df = df.dropna(subset=[
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ])

    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    for col in feature_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=feature_cols)

    return df
# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Dataset loading error: {e}")
    st.stop()

# -------------------------------------------------
# Required Columns Check
# -------------------------------------------------
required_columns = [
    "track_name",
    "artists",
    "album_name",
    "energy",
    "danceability",
    "valence",
    "tempo",
    "acousticness",
    "instrumentalness"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns in dataset: {missing_cols}")
    st.stop()

# -------------------------------------------------
# User Input Section
# -------------------------------------------------
genres = st.multiselect(
    "Select Your Favorite Genres:",
    df["genre"].unique(),
    key="genre_select"
)

mood = st.selectbox(
    "Select Your Current Mood:",
    ["Happy", "Sad", "Chill", "Energetic"],
    key="mood_select"
)

activity = st.selectbox(
    "Select Your Activity:",
    ["Gym", "Study", "Party", "Relax"],
    key="activity_select"
)

liked_songs = st.text_area(
    "Enter Previously Liked Songs (comma separated):",
    key="liked_songs_input"
)

# -------------------------------------------------
# Recommendation Button
# -------------------------------------------------
if st.button("Generate Recommendations", key="generate_btn"):

    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    # -----------------------------
    # 1️⃣ Build User Taste Vector
    # -----------------------------
    if genres:
        user_df = df[df["genre"].isin(genres)]
    else:
        user_df = df.copy()

    if user_df.empty:
        st.warning("No songs found for selected genre.")
        st.stop()

    user_vector = user_df[feature_cols].mean().values.reshape(1, -1)

    # -----------------------------
    # 2️⃣ Context Weighting
    # -----------------------------
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

    # -----------------------------
    # 3️⃣ Content Similarity
    # -----------------------------
    similarity_scores = cosine_similarity(
        user_vector,
        weighted_features
    )

    df["content_score"] = similarity_scores.flatten()

    # -----------------------------
    # 4️⃣ Collaborative Score
    # -----------------------------
    if "popularity" in df.columns:
        df["collab_score"] = df["popularity"] / df["popularity"].max()
    else:
        df["collab_score"] = 0.5

    # -----------------------------
    # 5️⃣ Final Hybrid Score
    # -----------------------------
    df["final_score"] = (
        0.4 * df["content_score"] +
        0.4 * df["collab_score"] +
        0.2 * df["content_score"]
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
            "album_name",
            "final_score"
        ]]
    )
