const labels = {
  overdue: "En retard",
  urgent: "Urgent",
  normal: "Normal",
  completed: "Terminee",
  cancelled: "Annulee",
  archived: "Archivee",
};

export default function ReminderStatusBadge({ reminder }) {
  return (
    <span className="status-badge" style={{ borderColor: reminder.color }}>
      <span className="status-dot" style={{ backgroundColor: reminder.color }} />
      {labels[reminder.expert_state] || reminder.expert_state}
    </span>
  );
}
