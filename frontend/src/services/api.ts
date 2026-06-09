import axios from "axios";

const api = axios.create({
  baseURL: "/_/backend",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
