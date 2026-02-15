import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations(df, genres, mood, activity):

    feature_cols = [
        "energy",
        "danceability",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness"
    ]

    # Filter by genre
    if genres:
        user_df = df[df["genre"].isin(genres)]
   

    if user_df.empty:
        return None

    # Build user vector
    user_vector = user_df[feature_cols].mean().values.reshape(1, -1)

    # Context weighting
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

    similarity = cosine_similarity(user_vector, weighted_features)

    df["content_score"] = similarity.flatten()

    # Collaborative score
    if "popularity" in df.columns:
        df["collab_score"] = df["popularity"] / df["popularity"].max()
    else:
        df["collab_score"] = 0.5

    # Final score
    df["final_score"] = (
        0.6 * df["content_score"] +
        0.4 * df["collab_score"]
    )

    recommendations = df.sort_values(
        by="final_score",
        ascending=False
    ).head(10)

    return recommendations
