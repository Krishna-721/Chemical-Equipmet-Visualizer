import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// Attach auth header
api.interceptors.request.use(config => {
  const auth = localStorage.getItem("auth");
  if (auth) {
    config.headers.Authorization = `Basic ${auth}`;
  }
  return config;
});

// Auth helpers
export function setAuth(username, password) {
  const token = btoa(`${username}:${password}`);
  localStorage.setItem("auth", token);
}

export function clearAuth() {
  localStorage.removeItem("auth");
}

export function isAuthenticated() {
  return !!localStorage.getItem("auth");
}

export default api;
