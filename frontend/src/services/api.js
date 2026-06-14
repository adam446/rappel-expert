const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "rappel_expert_token";

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearAccessToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function apiRequest(path, options = {}) {
  const token = getAccessToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = "Une erreur est survenue.";
    try {
      const body = await response.json();
      if (typeof body.detail === "string") message = body.detail;
      else if (Array.isArray(body.detail) && body.detail[0]?.msg) {
        message = body.detail[0].msg.replace(/^Value error, /, "");
      }
    } catch {
      // La reponse ne contient pas de JSON exploitable.
    }
    if (response.status === 401 && path === "/auth/me") {
      clearAccessToken();
      window.dispatchEvent(new Event("auth:unauthorized"));
    }
    throw new Error(message);
  }

  return response.status === 204 ? null : response.json();
}
