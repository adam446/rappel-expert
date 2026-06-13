import { apiRequest } from "./api.js";

export const getRecurringTasks = () => apiRequest("/recurring-tasks");

export const createRecurringTask = (data) =>
  apiRequest("/recurring-tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const updateRecurringTask = (id, data) =>
  apiRequest(`/recurring-tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const archiveRecurringTask = (id) =>
  apiRequest(`/recurring-tasks/${id}`, { method: "DELETE" });
