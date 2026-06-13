export default function RecurringTaskList({ tasks, onEdit, onArchive }) {
  return (
    <section className="panel recurring-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Configuration</p>
          <h2>Taches recurrentes</h2>
        </div>
        <span className="count">{tasks.length}</span>
      </div>

      <div className="task-list">
        {tasks.length === 0 && <p className="empty">Aucune serie creee.</p>}
        {tasks.map((task) => (
          <article className="task-row" key={task.id}>
            <div>
              <strong>{task.title}</strong>
              <span>{task.start_date} au {task.end_date}</span>
              <span>{task.frequency === "monthly" ? "Mensuelle" : "Hebdomadaire"} · {task.status}</span>
            </div>
            <div className="row-actions">
              <button className="text-button" onClick={() => onEdit(task)}>Modifier</button>
              {task.status !== "archived" && (
                <button className="text-button danger" onClick={() => onArchive(task.id)}>Archiver</button>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
