import os
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd

from app.config import settings


class RecommendationEngine:
    """Singleton AI recommendation engine with O(1) index lookup."""

    def __init__(self):
        self.movies_df: pd.DataFrame | None = None
        self.similarity_matrix: np.ndarray | None = None
        self.is_loaded: bool = False
        self._index_map: Dict[int, int] = {}

    def load(self, models_dir: str | None = None):
        models_dir = models_dir or settings.MODELS_DIR
        meta_path = os.path.join(models_dir, "movies_metadata.pkl")
        matrix_path = os.path.join(models_dir, "similarity_matrix.pkl")

        if not os.path.exists(meta_path) or not os.path.exists(matrix_path):
            print("[-] Model files not found. Engine running in fallback mode.")
            return

        self.movies_df = joblib.load(meta_path)
        self.similarity_matrix = joblib.load(matrix_path)

        self._index_map = {
            int(row["id"]): idx for idx, row in self.movies_df.iterrows()
        }

        self.is_loaded = True
        print(
            f"[+] Engine loaded: {len(self.movies_df)} movies, "
            f"matrix {self.similarity_matrix.shape}"
        )

    def _row_to_dict(self, row, score: float | None = None) -> Dict[str, Any]:
        genres = row.get("genres_clean", [])
        if isinstance(genres, list):
            genre_names = genres
        else:
            genre_names = []

        result = {
            "movie_id": int(row["id"]),
            "title": str(row["title"]),
            "vote_average": float(row["vote_average"]),
            "popularity": float(row.get("popularity", 0)),
            "release_date": str(row.get("release_date", "") or ""),
            "overview": str(row.get("overview", "") or ""),
            "poster_path": str(row.get("poster_path", "") or "") or None,
            "genres": genre_names,
        }
        if score is not None:
            result["confidence_score"] = round(float(score), 4)
        return result

    def get_recommendations(
        self, movie_id: int, top_n: int = 10
    ) -> List[Dict[str, Any]]:
        if not self.is_loaded:
            return self._fallback_popular(top_n)

        idx = self._index_map.get(movie_id)
        if idx is None:
            return []

        scores = list(enumerate(self.similarity_matrix[idx]))
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, score in scores[1 : top_n + 1]:
            row = self.movies_df.iloc[i]
            results.append(self._row_to_dict(row, score))
        return results

    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any] | None:
        if self.movies_df is None:
            return None
        idx = self._index_map.get(movie_id)
        if idx is None:
            return None
        return self._row_to_dict(self.movies_df.iloc[idx])

    def _fallback_popular(self, top_n: int) -> List[Dict[str, Any]]:
        if self.movies_df is None:
            return []
        top = self.movies_df.nlargest(top_n, "popularity")
        return [
            {**self._row_to_dict(r), "confidence_score": 0.5}
            for _, r in top.iterrows()
        ]

    def get_popular(self, top_n: int = 20) -> List[Dict[str, Any]]:
        return self._fallback_popular(top_n)

    def search_by_title(self, query: str, top_n: int = 10) -> List[Dict[str, Any]]:
        if self.movies_df is None:
            return []
        q = query.lower().strip()
        mask = self.movies_df["title"].str.lower().str.contains(q, na=False)
        results = self.movies_df[mask].head(top_n)
        return [self._row_to_dict(r) for _, r in results.iterrows()]


ai_engine = RecommendationEngine()
