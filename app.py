import streamlit as st
import urllib.parse

from utils import load_and_clean_data
from recommender import generate_recommendations

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Music Recommender", layout="wide")

st.title("🎵 Intelligent Music Recommendation System")

# ---------------- SESSION STATE ----------------
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


# ---------------- DATA LOADING ----------------
@st.cache_data
def get_data():
    return load_and_clean_data("dataset.csv")


df = get_data()


# ---------------- UTILITY FUNCTIONS ----------------
def get_links(track, artist):
    query = urllib.parse.quote(f"{track} {artist}")
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    spotify_url = f"https://open.spotify.com/search/{query}"
    return youtube_url, spotify_url


def display_song_details(song):
    st.write(f"🎤 **Artist:** {song['artists']}")
    st.write(f"🎼 **Genre:** {song['genre']}")
    st.write(f"⭐ Score: {song['confidence']:.2f}")


# ---------------- SIDEBAR INPUT SECTION ----------------
with st.sidebar:
    st.header("🎧 Group Preferences")

    genres = st.multiselect(
        "Select Genre",
        sorted(df["genre"].dropna().unique())
    )

    mood = st.selectbox(
        "Select Mood",
        ["Happy", "Sad", "Chill", "Energetic"]
    )

    activity = st.selectbox(
        "Select Activity",
        ["Party", "Gym", "Study", "Relax"]
    )

    liked_songs = st.text_area("Previously Liked Songs")

    generate = st.button("Generate Recommendations")


# ---------------- RECOMMENDATION ENGINE ----------------
def run_recommendation():
    if not liked_songs.strip():
        st.info("No listening history found. Using context-based filtering.")

    recs = generate_recommendations(df, genres, mood, activity)

    if recs is None or recs.empty:
        st.warning("No songs found for selected preferences.")
        return None

    recs["confidence"] = (recs["final_score"] * 100).round(2)
    return recs


# ---------------- GENERATE BUTTON ACTION ----------------
if generate:
    st.session_state.recommendations = run_recommendation()


# ---------------- MAIN DISPLAY SECTION ----------------
if st.session_state.recommendations is not None:

    recs = st.session_state.recommendations

    # ---------------- TOP SECTION ----------------
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("🔥 Top Recommendations")

        st.dataframe(
            recs.head(10)[["track_name", "artists", "genre", "confidence"]]
        )

    with col2:
        st.subheader("🎵 Song Selection")

        selected_song = st.selectbox(
            "Pick any song to play",
            recs["track_name"].tolist()
        )

        song = recs[recs["track_name"] == selected_song].iloc[0]

        display_song_details(song)

        youtube_url, spotify_url = get_links(song["track_name"], song["artists"])

        c1, c2 = st.columns(2)

        with c1:
            st.link_button("▶️ Play on YouTube", youtube_url)

        with c2:
            st.link_button("🎵 Open in Spotify", spotify_url)

    # ---------------- WHY SECTION ----------------
    st.subheader("🔎 Why These Songs?")

    st.markdown(
        f"""
        Based on your selected preferences:
        - Genre: **{', '.join(genres) if genres else 'All'}**
        - Mood: **{mood}**
        - Activity: **{activity}**

        The system uses a **hybrid scoring model**:
        - Content similarity
        - Genre matching
        - Popularity weighting
        """
    )
