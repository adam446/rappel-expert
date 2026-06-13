import { useMemo, useState } from "react";

const weekdays = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];
const monthFormatter = new Intl.DateTimeFormat("fr-CA", { month: "long", year: "numeric" });
const amountFormatter = new Intl.NumberFormat("fr-CA", {
  style: "currency",
  currency: "CAD",
});

const dateKey = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

export default function ReminderCalendar({ reminders, onSelect }) {
  const [visibleMonth, setVisibleMonth] = useState(() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), 1);
  });

  const remindersByDate = useMemo(() => {
    return reminders.reduce((grouped, reminder) => {
      grouped[reminder.due_date] ||= [];
      grouped[reminder.due_date].push(reminder);
      return grouped;
    }, {});
  }, [reminders]);

  const days = useMemo(() => {
    const year = visibleMonth.getFullYear();
    const month = visibleMonth.getMonth();
    const firstWeekday = (new Date(year, month, 1).getDay() + 6) % 7;
    const lastDay = new Date(year, month + 1, 0).getDate();
    const result = [];
    for (let index = 0; index < firstWeekday; index += 1) result.push(null);
    for (let day = 1; day <= lastDay; day += 1) result.push(new Date(year, month, day));
    while (result.length % 7 !== 0) result.push(null);
    return result;
  }, [visibleMonth]);

  const moveMonth = (offset) => {
    setVisibleMonth((current) => new Date(current.getFullYear(), current.getMonth() + offset, 1));
  };

  return (
    <section className="calendar-section">
      <div className="calendar-toolbar">
        <div>
          <p className="eyebrow">Vue mensuelle</p>
          <h2>{monthFormatter.format(visibleMonth)}</h2>
        </div>
        <div className="calendar-actions">
          <button className="icon-button" title="Mois precedent" onClick={() => moveMonth(-1)} aria-label="Mois precedent">←</button>
          <button className="button secondary compact" onClick={() => setVisibleMonth(new Date(new Date().getFullYear(), new Date().getMonth(), 1))}>Aujourd'hui</button>
          <button className="icon-button" title="Mois suivant" onClick={() => moveMonth(1)} aria-label="Mois suivant">→</button>
        </div>
      </div>

      <div className="calendar-grid weekdays">
        {weekdays.map((day) => <div key={day}>{day}</div>)}
      </div>
      <div className="calendar-grid month-grid">
        {days.map((day, index) => {
          if (!day) return <div className="calendar-day muted-day" key={`empty-${index}`} />;
          const key = dateKey(day);
          const dayReminders = remindersByDate[key] || [];
          return (
            <div className="calendar-day" key={key}>
              <span className="day-number">{day.getDate()}</span>
              <div className="day-events">
                {dayReminders.slice(0, 3).map((reminder) => (
                  <button
                    className="calendar-event"
                    key={reminder.id}
                    style={{ borderLeftColor: reminder.color }}
                    onClick={() => onSelect(reminder)}
                    title={`${reminder.title} - ${reminder.expert_state}`}
                  >
                    <strong>{reminder.title}</strong>
                    <small>
                      {reminder.amount == null ? reminder.expert_state : amountFormatter.format(reminder.amount)}
                    </small>
                  </button>
                ))}
                {dayReminders.length > 3 && <span className="more-events">+{dayReminders.length - 3}</span>}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
