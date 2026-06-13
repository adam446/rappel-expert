import { ReminderList } from "./OverdueReminders.jsx";

export default function UpcomingReminders({ reminders, onSelect }) {
  return <ReminderList title="Taches urgentes" eyebrow="7 prochains jours" reminders={reminders} onSelect={onSelect} />;
}
