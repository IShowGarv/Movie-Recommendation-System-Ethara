import json
import re

import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")


def parse_json_column(val, key="name", limit=None):
    """Safely parses JSON-like string columns (genres, keywords, cast)."""
    if pd.isna(val):
        return []
    try:
        data = json.loads(val)
        names = [item[key].strip().lower().replace(" ", "") for item in data]
        return names[:limit] if limit else names
    except Exception:
        return []


def extract_director(crew_val):
    """Extracts director name(s) from raw crew JSON string."""
    if pd.isna(crew_val):
        return []
    try:
        data = json.loads(crew_val)
        return [
            item["name"].strip().lower().replace(" ", "")
            for item in data
            if item.get("job") == "Director"
        ]
    except Exception:
        return []


def normalize_text(text):
    """Normalizes overview/tagline text with stemming."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(stemmer.stem(word) for word in text.split())


def build_feature_soup(df: pd.DataFrame) -> pd.DataFrame:
    """Engineers a unified 'soup' text feature from all metadata columns."""
    df = df.copy()
    df["genres_clean"] = df["genres"].apply(parse_json_column)
    df["keywords_clean"] = df["keywords"].apply(parse_json_column)
    df["cast_clean"] = df["cast"].apply(lambda x: parse_json_column(x, limit=4))
    df["director_clean"] = df["crew"].apply(extract_director)
    df["overview_clean"] = df["overview"].apply(normalize_text)
    df["tagline_clean"] = df["tagline"].apply(normalize_text)

    def build_row_soup(row):
        director_weighted = row["director_clean"] * 3
        parts = (
            row["genres_clean"]
            + row["keywords_clean"]
            + row["cast_clean"]
            + director_weighted
            + [row["overview_clean"]]
            + [row["tagline_clean"]]
        )
        return " ".join(parts)

    df["soup"] = df.apply(build_row_soup, axis=1)
    return df
