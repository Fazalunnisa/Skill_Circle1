// CENTRAL API CONFIGURATION
// When running locally, it talks to localhost:8000
// When deployed, it talks to your Render.com URL
const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : ""; // In production on Vercel, use relative paths for speed
