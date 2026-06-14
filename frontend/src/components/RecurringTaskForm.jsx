import { useEffect, useState } from "react";

const emptyForm = {
  title: "",
  description: "",
  amount: "",
  start_date: "",
  end_date: "",
  frequency: "monthly",
  status: "active",
};

export default function RecurringTaskForm({ editingTask, onCancel, onSubmit }) {
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm(
      editingTask
        ? {
            ...emptyForm,
            ...editingTask,
            amount: editingTask.amount ?? "",
          }
        : emptyForm,
    );
  }, [editingTask]);

  const update = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    try {
      const startDay = Number(form.start_date.slice(-2));
      await onSubmit({
        ...form,
        amount: form.amount === "" ? null : Number(form.amount),
        day_of_month: startDay,
      });
      if (!editingTask) setForm(emptyForm);
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="task-form" onSubmit={submit}>
      <div className="section-heading">
        <div>
          <p className="eyebrow">Serie de rappels</p>
          <h2>{editingTask ? "Modifier la tache" : "Nouvelle tache recurrente"}</h2>
        </div>
      </div>

      <label className="field field-wide">
        <span>Titre</span>
        <input name="title" value={form.title} onChange={update} required />
      </label>

      <label className="field field-wide">
        <span>Description</span>
        <textarea name="description" value={form.description || ""} onChange={update} rows="3" />
      </label>

      <label className="field field-wide">
        <span>Montant ($)</span>
        <input name="amount" type="number" min="0" step="0.01" value={form.amount} onChange={update} />
      </label>

      <label className="field">
        <span>Date de debut</span>
        <input name="start_date" type="date" value={form.start_date} onChange={update} required />
      </label>

      <label className="field">
        <span>Date de fin</span>
        <input name="end_date" type="date" value={form.end_date} onChange={update} required />
      </label>

      <label className="field">
        <span>Frequence</span>
        <select name="frequency" value={form.frequency} onChange={update}>
          <option value="monthly">Mensuelle</option>
          <option value="weekly">Hebdomadaire</option>
        </select>
      </label>

      <label className="field">
        <span>Statut</span>
        <select name="status" value={form.status} onChange={update}>
          <option value="active">Active</option>
          <option value="cancelled">Annulee</option>
          <option value="archived">Archivee</option>
        </select>
      </label>

      <div className="form-actions field-wide">
        {editingTask && <button type="button" className="button secondary" onClick={onCancel}>Annuler</button>}
        <button className="button primary" disabled={saving}>
          {saving ? "Enregistrement..." : editingTask ? "Mettre a jour" : "Creer et generer"}
        </button>
      </div>
    </form>
  );
}
