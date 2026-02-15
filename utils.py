import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Fix genre column name
    if "track_genre" in df.columns:
        df = df.rename(columns={"track_genre": "genre"})

    # Remove duplicates
    df = df.drop_duplicates(subset=["track_name", "artists"])

    # Feature columns
    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    # Convert numeric
    for col in feature_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop missing rows
    df = df.dropna(subset=feature_cols)

    return df
