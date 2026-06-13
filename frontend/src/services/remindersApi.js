import { apiRequest } from "./api.js";

export const getReminders = () => apiRequest("/reminders");
export const getOverdueReminders = () => apiRequest("/reminders/overdue");
export const getUpcomingReminders = () => apiRequest("/reminders/upcoming");

export const updateReminder = (id, data) =>
  apiRequest(`/reminders/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });

export const completeReminder = (id) =>
  apiRequest(`/reminders/${id}/complete`, { method: "PUT" });

export const deleteReminder = (id) =>
  apiRequest(`/reminders/${id}`, { method: "DELETE" });

export const applyExpertRules = () =>
  apiRequest("/expert-rules/apply", { method: "POST" });
