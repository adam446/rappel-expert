import { useCallback, useEffect, useMemo, useState } from "react";
import OverdueReminders from "./components/OverdueReminders.jsx";
import RecurringTaskForm from "./components/RecurringTaskForm.jsx";
import RecurringTaskList from "./components/RecurringTaskList.jsx";
import ReminderCalendar from "./components/ReminderCalendar.jsx";
import ReminderDetail from "./components/ReminderDetail.jsx";
import UpcomingReminders from "./components/UpcomingReminders.jsx";
import {
  archiveRecurringTask,
  createRecurringTask,
  getRecurringTasks,
  updateRecurringTask,
} from "./services/recurringTasksApi.js";
import {
  applyExpertRules,
  completeReminder,
  deleteReminder,
  getReminders,
  updateReminder,
} from "./services/remindersApi.js";
import "./styles/main.css";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [selectedReminder, setSelectedReminder] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [view, setView] = useState("calendar");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    setError("");
    try {
      const [taskData, reminderData] = await Promise.all([
        getRecurringTasks(),
        getReminders(),
      ]);
      setTasks(taskData);
      setReminders(reminderData);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  const overdue = useMemo(() => reminders.filter((item) => item.expert_state === "overdue"), [reminders]);
  const urgent = useMemo(() => reminders.filter((item) => item.expert_state === "urgent"), [reminders]);
  const completed = useMemo(() => reminders.filter((item) => item.expert_state === "completed"), [reminders]);

  const runAction = async (action, closeModal = false) => {
    setError("");
    try {
      await action();
      if (closeModal) setSelectedReminder(null);
      await loadData();
    } catch (actionError) {
      setError(actionError.message);
    }
  };

  const saveTask = async (data) => {
    await runAction(async () => {
      if (editingTask) await updateRecurringTask(editingTask.id, data);
      else await createRecurringTask(data);
      setEditingTask(null);
      setView("calendar");
    });
  };

  const saveReminder = async (id, data) => {
    await runAction(async () => updateReminder(id, data), true);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-mark">R</div>
        <div className="brand-copy">
          <strong>Rappel Expert</strong>
          <span>Gestion des taches recurrentes</span>
        </div>
        <nav className="view-tabs" aria-label="Vues principales">
          <button className={view === "calendar" ? "active" : ""} onClick={() => setView("calendar")}>Calendrier</button>
          <button className={view === "tasks" ? "active" : ""} onClick={() => setView("tasks")}>Taches</button>
        </nav>
        <button className="button secondary sync-button" onClick={() => runAction(applyExpertRules)}>Actualiser les regles</button>
      </header>

      <main className="app-content">
        <section className="page-intro">
          <div>
            <p className="eyebrow">Tableau de bord</p>
            <h1>Vos echeances, clairement.</h1>
          </div>
          <button className="button primary" onClick={() => { setEditingTask(null); setView("tasks"); }}>+ Nouvelle tache</button>
        </section>

        {error && <div className="alert" role="alert">{error}</div>}

        <section className="stats-grid">
          <article><span>Total</span><strong>{reminders.length}</strong><small>rappels generes</small></article>
          <article className="stat-overdue"><span>En retard</span><strong>{overdue.length}</strong><small>a traiter</small></article>
          <article className="stat-urgent"><span>Urgentes</span><strong>{urgent.length}</strong><small>dans les 7 jours</small></article>
          <article className="stat-completed"><span>Terminees</span><strong>{completed.length}</strong><small>rappels completes</small></article>
        </section>

        {loading ? (
          <div className="loading">Chargement...</div>
        ) : view === "calendar" ? (
          <>
            <ReminderCalendar reminders={reminders.filter((item) => item.expert_state !== "archived")} onSelect={setSelectedReminder} />
            <div className="lists-grid">
              <OverdueReminders reminders={overdue} onSelect={setSelectedReminder} />
              <UpcomingReminders reminders={urgent} onSelect={setSelectedReminder} />
            </div>
          </>
        ) : (
          <div className="management-grid">
            <section className="panel form-panel">
              <RecurringTaskForm editingTask={editingTask} onCancel={() => setEditingTask(null)} onSubmit={saveTask} />
            </section>
            <RecurringTaskList
              tasks={tasks}
              onEdit={setEditingTask}
              onArchive={(id) => {
                if (window.confirm("Archiver cette serie et ses rappels ?")) {
                  runAction(() => archiveRecurringTask(id));
                }
              }}
            />
          </div>
        )}
      </main>

      <ReminderDetail
        reminder={selectedReminder}
        onClose={() => setSelectedReminder(null)}
        onUpdate={saveReminder}
        onComplete={(id) => runAction(() => completeReminder(id), true)}
        onDelete={(id) => {
          if (window.confirm("Supprimer ce rappel ?")) runAction(() => deleteReminder(id), true);
        }}
      />
    </div>
  );
}
