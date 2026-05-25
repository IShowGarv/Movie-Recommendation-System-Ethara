export interface Movie {
  movie_id: number;
  title: string;
  vote_average: number;
  popularity: number;
  release_date: string;
  overview: string;
  confidence_score?: number;
  poster_path?: string | null;
  genres?: string[];
}

export interface User {
  name: string;
  email: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface WatchlistItem {
  movie_id: number;
  title: string;
  added_at?: string;
}
