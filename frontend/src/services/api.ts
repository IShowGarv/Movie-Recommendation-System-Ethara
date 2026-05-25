import axios from "axios";
import { Movie } from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getPopularMovies = (limit = 20) =>
  api.get<Movie[]>(`/api/movies/popular?limit=${limit}`);

export const getMovie = (movieId: number) =>
  api.get<Movie>(`/api/movies/${movieId}`);

export const searchMovies = (q: string, limit = 10) =>
  api.get<Movie[]>(
    `/api/movies/search?q=${encodeURIComponent(q)}&limit=${limit}`
  );

export const getRecommendations = (movieId: number, limit = 10) =>
  api.get<Movie[]>(
    `/api/recommend?movie_id=${movieId}&limit=${limit}`
  );

export const register = (name: string, email: string, password: string) =>
  api.post("/api/auth/register", { name, email, password });

export const login = (email: string, password: string) =>
  api.post("/api/auth/login", { email, password });

export const getWatchlist = () => api.get("/api/user/watchlist");

export const addToWatchlist = (movie_id: number, title: string) =>
  api.post("/api/user/watchlist", { movie_id, title });

export const removeFromWatchlist = (movieId: number) =>
  api.delete(`/api/user/watchlist/${movieId}`);

export default api;
