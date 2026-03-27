import streamlit as st
import pandas as pd
from utils import load_and_clean_data
from recommender import generate_recommendations
import urllib.parse
st.set_page_config(page_title="Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")


# ---------------- SESSION STATE FIX ----------------
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None




# Load data
df = load_and_clean_data("dataset.csv")



# ---------------- HELPER FUNCTION ----------------
def get_links(track, artist):
    query = urllib.parse.quote(f"{track} {artist}")

    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    spotify_url = f"https://open.spotify.com/search/{query}"

    return youtube_url, spotify_url







# Layout
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("🎧 group Preferences")

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
    
# ---------------- GENERATE ----------------
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




              # ---------------- GENERATE ONCE ----------------
if generate:
    if not liked_songs.strip():
        st.info("No listening history found. Using context-based filtering.")

    recs = generate_recommendations(df, genres, mood, activity)

    if recs is None or recs.empty:
        st.warning("No songs found.")
    else:
        st.session_state.recommendations = recs


# ---------------- DISPLAY ALWAYS ----------------
if st.session_state.recommendations is not None:

    recs = st.session_state.recommendations.copy()

    recs["confidence"] = (recs["final_score"] * 100).round(2)

    # ---------------- TOP SONGS ----------------
    st.subheader("🔥 Top Recommendations")

    st.dataframe(
        recs.head(10)[[
            "track_name",
            "artists",
            "genre",
            "confidence"
        ]]
    )

    # ---------------- FULL SONG LIST ----------------
    st.subheader("🎵 All Available Songs")

    selected_song = st.selectbox(
        "Pick any song to play",
        recs["track_name"].tolist()
    )

    song = recs[recs["track_name"] == selected_song].iloc[0]

    st.write(f"🎤 **Artist:** {song['artists']}")
    st.write(f"🎼 **Genre:** {song['genre']}")
    st.write(f"⭐ Score: {song['confidence']:.2f}")

    # ---------------- PLAY LINKS ----------------
    youtube_url, spotify_url = get_links(song["track_name"], song["artists"])

    col1, col2 = st.columns(2)

    with col1:
        st.link_button("▶️ Play on YouTube", youtube_url)

    with col2:
        st.link_button("🎵 Open in Spotify", spotify_url)

        # ---------------- WHY SECTION ----------------




        

        st.subheader("🔎 Why These Songs?")
        st.markdown(f"""
        Based on your love for **{', '.join(genres) if genres else 'various genres'}**,
        your **{mood} mood**, and **{activity} activity**,
        we prioritized high-energy and high-valence tracks.
        """)
