import { useEffect, useState } from "react";
import { getAdminDashboard } from "../services/adminApi.js";

export default function AdminDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getAdminDashboard()
      .then(setDashboard)
      .catch((requestError) => setError(requestError.message));
  }, []);

  if (error) return <div className="alert" role="alert">{error}</div>;
  if (!dashboard) return <div className="loading">Chargement du tableau de bord...</div>;

  const { stats, users } = dashboard;

  return (
    <>
      <section className="admin-stats">
        <article><span>Utilisateurs</span><strong>{stats.users}</strong></article>
        <article><span>Comptes actifs</span><strong>{stats.active_users}</strong></article>
        <article><span>Taches</span><strong>{stats.recurring_tasks}</strong></article>
        <article><span>Rappels</span><strong>{stats.reminders}</strong></article>
      </section>

      <section className="panel admin-users-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Administration</p>
            <h2>Utilisateurs inscrits</h2>
          </div>
          <span className="count">{users.length}</span>
        </div>
        <div className="admin-table-wrap">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Role</th>
                <th>Statut</th>
                <th>Taches</th>
                <th>Rappels</th>
                <th>Inscription</th>
              </tr>
            </thead>
            <tbody>
              {users.map((account) => (
                <tr key={account.id}>
                  <td>
                    <strong>{account.full_name}</strong>
                    <span>@{account.username} · {account.email}</span>
                  </td>
                  <td>{account.is_admin ? "Admin" : "Utilisateur"}</td>
                  <td>
                    <span className={`account-status ${account.is_active ? "active" : "inactive"}`}>
                      {account.is_active ? "Actif" : "Inactif"}
                    </span>
                  </td>
                  <td>{account.task_count}</td>
                  <td>{account.reminder_count}</td>
                  <td>{new Date(account.created_at).toLocaleDateString("fr-CA")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}
