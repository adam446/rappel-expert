import { useEffect, useState } from "react";
import ReminderStatusBadge from "./ReminderStatusBadge.jsx";

export default function ReminderDetail({ reminder, onClose, onComplete, onDelete, onUpdate }) {
  const [form, setForm] = useState(null);

  useEffect(() => {
    setForm(reminder ? {
      title: reminder.title,
      description: reminder.description || "",
      amount: reminder.amount ?? "",
      due_date: reminder.due_date,
      status: reminder.status,
    } : null);
  }, [reminder]);

  if (!reminder || !form) return null;

  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  const save = async (event) => {
    event.preventDefault();
    await onUpdate(reminder.id, {
      ...form,
      amount: form.amount === "" ? null : Number(form.amount),
    });
  };

  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <section className="modal" onMouseDown={(event) => event.stopPropagation()} role="dialog" aria-modal="true">
        <div className="modal-header">
          <div>
            <p className="eyebrow">Rappel #{reminder.id}</p>
            <h2>Detail du rappel</h2>
          </div>
          <button className="icon-button" onClick={onClose} aria-label="Fermer" title="Fermer">×</button>
        </div>

        <ReminderStatusBadge reminder={reminder} />

        <form className="detail-form" onSubmit={save}>
          <label className="field"><span>Titre</span><input name="title" value={form.title} onChange={update} required /></label>
          <label className="field"><span>Description</span><textarea name="description" value={form.description} onChange={update} rows="3" /></label>
          <div className="detail-grid">
            <label className="field"><span>Montant ($)</span><input name="amount" type="number" min="0" step="0.01" value={form.amount} onChange={update} /></label>
            <label className="field"><span>Date</span><input name="due_date" type="date" value={form.due_date} onChange={update} required /></label>
          </div>
          <label className="field">
            <span>Statut</span>
            <select name="status" value={form.status} onChange={update}>
              <option value="pending">En attente</option>
              <option value="completed">Completee</option>
              <option value="cancelled">Annulee</option>
              <option value="archived">Archivee</option>
            </select>
          </label>

          <div className="modal-actions">
            <button type="button" className="button danger-button" onClick={() => onDelete(reminder.id)}>Supprimer</button>
            {reminder.status !== "completed" && <button type="button" className="button success" onClick={() => onComplete(reminder.id)}>Completer</button>}
            <button className="button primary">Enregistrer</button>
          </div>
        </form>
      </section>
    </div>
  );
}
