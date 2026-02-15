import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")

    # Make all column names lowercase
    df.columns = df.columns.str.lower().str.strip()

    # If dataset has track_genre, rename it to genre
    if "track_genre" in df.columns:
        df = df.rename(columns={"track_genre": "genre"})

    # Remove duplicates
    df = df.drop_duplicates(subset=["track_name", "artists"])

    # Required numeric features
    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    # Convert to numeric
    for col in feature_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop missing rows
    df = df.dropna(subset=feature_cols)

    return df
