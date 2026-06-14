import { apiRequest } from "./api.js";

export function getAdminDashboard() {
  return apiRequest("/admin/dashboard");
}
