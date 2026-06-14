import { apiRequest, clearAccessToken, setAccessToken } from "./api.js";

export async function login(username, password) {
  const response = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  setAccessToken(response.access_token);
  return response.user;
}

export async function signup(fullName, email, username, password) {
  const response = await apiRequest("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ full_name: fullName, email, username, password }),
  });
  setAccessToken(response.access_token);
  return response.user;
}

export function getCurrentUser() {
  return apiRequest("/auth/me");
}

export function forgotPassword(email) {
  return apiRequest("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export function resetPassword(token, password) {
  return apiRequest("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, password }),
  });
}

export function logout() {
  clearAccessToken();
}
