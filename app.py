import streamlit as st
import pandas as pd

st.set_page_config(page_title="Intelligent Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")

# ===============================
# LOAD DATA
# ===============================

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset.csv")
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# ===============================
# CHECK REQUIRED COLUMNS
# ===============================

required_columns = ['track_name', 'artists', 'album_name']

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"The following required columns are missing in the CSV: {missing_columns}")
    st.write("Available columns in your dataset:")
    st.write(df.columns.tolist())
    st.stop()

# ===============================
# USER INPUT SECTION
# ===============================

st.subheader("Select Your Preferences")

# Genre Selection (if exists)
if "genre" in df.columns:
    genres = st.multiselect(
        "Select Your Favorite Genres:",
        options=sorted(df["genre"].dropna().unique())
    )
else:
    genres = []

# Mood Selection
mood = st.selectbox(
    "Select Your Mood:",
    ["Happy", "Sad", "Chill", "Energetic"]
)

# Activity Selection
activity = st.selectbox(
    "Select Your Activity:",
    ["Gym", "Study", "Party", "Relax"]
)

# Previously liked songs
liked_songs = st.text_area(
    "Enter Previously Liked Songs (comma separated)"
)

# ===============================
# RECOMMENDATION LOGIC
# ===============================

if st.button("Generate Recommendations"):

    filtered_df = df.copy()

    # Filter by genre if selected
    if genres and "genre" in df.columns:
        filtered_df = filtered_df[filtered_df["genre"].isin(genres)]

    # Mood-based filtering example (if valence exists)
    if "valence" in df.columns:
        if mood == "Happy":
            filtered_df = filtered_df[filtered_df["valence"] > 0.6]
        elif mood == "Sad":
            filtered_df = filtered_df[filtered_df["valence"] < 0.4]

    # Activity-based filtering example (if energy exists)
    if "energy" in df.columns:
        if activity == "Gym":
            filtered_df = filtered_df[filtered_df["energy"] > 0.7]
        elif activity == "Relax":
            filtered_df = filtered_df[filtered_df["energy"] < 0.5]

    # Show results
    if filtered_df.empty:
        st.warning("No recommendations found. Try changing preferences.")
    else:
        st.success("Recommended Song
