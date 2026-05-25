import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pipeline import build_feature_soup


def run_pipeline():
    print("[*] Loading datasets...")
    movies_df = pd.read_csv("dataset/tmdb_5000_movies.csv")
    credits_df = pd.read_csv("dataset/tmdb_5000_credits.csv")

    df = movies_df.merge(credits_df, left_on="id", right_on="movie_id")
    print(f"[*] Merged dataset: {len(df)} movies")

    if "title_x" in df.columns:
        df["title"] = df["title_x"]
    elif "title" not in df.columns and "original_title" in df.columns:
        df["title"] = df["original_title"]

    if "poster_path" not in df.columns:
        df["poster_path"] = ""

    print("[*] Engineering feature soup...")
    df = build_feature_soup(df)

    print("[*] Fitting TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=15000,
        min_df=2,
        ngram_range=(1, 2),
    )
    tfidf_matrix = tfidf.fit_transform(df["soup"])
    print(f"[*] TF-IDF matrix shape: {tfidf_matrix.shape}")

    print("[*] Computing cosine similarity matrix (this takes ~30s)...")
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    processed_df = df[
        [
            "id",
            "title",
            "vote_average",
            "vote_count",
            "release_date",
            "popularity",
            "genres_clean",
            "overview",
            "poster_path",
        ]
    ].copy()
    processed_df["id"] = processed_df["id"].astype(int)
    processed_df = processed_df.reset_index(drop=True)

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(processed_df, os.path.join(models_dir, "movies_metadata.pkl"), compress=3)
    joblib.dump(
        similarity_matrix,
        os.path.join(models_dir, "similarity_matrix.pkl"),
        compress=5,
    )
    joblib.dump(tfidf, os.path.join(models_dir, "tfidf_vectorizer.pkl"), compress=3)

    print(f"[+] Pipeline complete. Models saved to {models_dir}/")
    print(f"    - movies_metadata.pkl: {len(processed_df)} records")
    print(f"    - similarity_matrix.pkl: {similarity_matrix.shape}")


if __name__ == "__main__":
    run_pipeline()
