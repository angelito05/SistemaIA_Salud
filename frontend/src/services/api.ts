import axios from "axios";

/**
 * Instancia base de Axios configurada para comunicarse con el backend FastAPI.
 * La URL base se lee de la variable de entorno NEXT_PUBLIC_API_URL.
 */
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 segundos (necesario para operaciones de OCR/IA)
});

// ─── Interceptor de Request ─────────────────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    // Aquí puedes agregar el token de autenticación si lo implementas
    // const token = localStorage.getItem("access_token");
    // if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// ─── Interceptor de Response ────────────────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const mensaje =
      error.response?.data?.detail ||
      error.message ||
      "Error de conexión con el servidor";
    console.error(`[API Error] ${mensaje}`);
    return Promise.reject(new Error(mensaje));
  }
);

export default api;
