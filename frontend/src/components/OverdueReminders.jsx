import ReminderStatusBadge from "./ReminderStatusBadge.jsx";

export default function OverdueReminders({ reminders, onSelect }) {
  return <ReminderList title="Taches en retard" eyebrow="A traiter" reminders={reminders} onSelect={onSelect} />;
}

function ReminderList({ title, eyebrow, reminders, onSelect }) {
  return (
    <section className="panel reminder-list-panel">
      <div className="section-heading">
        <div><p className="eyebrow">{eyebrow}</p><h2>{title}</h2></div>
        <span className="count">{reminders.length}</span>
      </div>
      <div className="compact-list">
        {reminders.length === 0 && <p className="empty">Aucun rappel.</p>}
        {reminders.map((reminder) => (
          <button className="compact-reminder" key={reminder.id} onClick={() => onSelect(reminder)}>
            <span><strong>{reminder.title}</strong><small>{reminder.due_date}</small></span>
            <ReminderStatusBadge reminder={reminder} />
          </button>
        ))}
      </div>
    </section>
  );
}

export { ReminderList };
