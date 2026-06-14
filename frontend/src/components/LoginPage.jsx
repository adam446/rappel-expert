import { useState } from "react";

export default function LoginPage({
  onLogin,
  onSignup,
  onForgotPassword,
  onResetPassword,
}) {
  const resetToken = new URLSearchParams(window.location.search).get("reset_token");
  const [mode, setMode] = useState(resetToken ? "reset" : "login");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");
    if ((mode === "signup" || mode === "reset") && password !== passwordConfirmation) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }
    setLoading(true);
    try {
      if (mode === "signup") {
        await onSignup(fullName, email, username, password);
      } else if (mode === "forgot") {
        const response = await onForgotPassword(email);
        setMessage(response.message);
      } else if (mode === "reset") {
        const response = await onResetPassword(resetToken, password);
        window.history.replaceState({}, "", window.location.pathname);
        setMessage(`${response.message} Vous pouvez maintenant vous connecter.`);
        setMode("login");
        setPassword("");
        setPasswordConfirmation("");
      } else {
        await onLogin(username, password);
      }
    } catch (loginError) {
      setError(loginError.message);
    } finally {
      setLoading(false);
    }
  };

  const changeMode = (nextMode) => {
    setMode(nextMode);
    setError("");
    setMessage("");
    setPassword("");
    setPasswordConfirmation("");
  };

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-brand">
          <div className="brand-mark">R</div>
          <div>
            <strong>Rappel Expert</strong>
            <span>Portail des rappels</span>
          </div>
        </div>

        <div className="login-heading">
          <p className="eyebrow">Compte utilisateur</p>
          <h1>
            {mode === "login" && "Bienvenue"}
            {mode === "signup" && "Creer un compte"}
            {mode === "forgot" && "Mot de passe oublie"}
            {mode === "reset" && "Nouveau mot de passe"}
          </h1>
          <p>
            {mode === "login" && "Connectez-vous pour gerer vos taches et rappels."}
            {mode === "signup" && "Inscrivez-vous avec votre email et un nom d'utilisateur."}
            {mode === "forgot" && "Nous vous enverrons un lien de reinitialisation par courriel."}
            {mode === "reset" && "Choisissez un nouveau mot de passe d'au moins 8 caracteres."}
          </p>
        </div>

        {mode !== "forgot" && mode !== "reset" && <div className="auth-tabs" role="tablist" aria-label="Authentification">
          <button
            type="button"
            className={mode === "login" ? "active" : ""}
            onClick={() => changeMode("login")}
          >
            Connexion
          </button>
          <button
            type="button"
            className={mode === "signup" ? "active" : ""}
            onClick={() => changeMode("signup")}
          >
            Inscription
          </button>
        </div>}

        {error && <div className="alert" role="alert">{error}</div>}
        {message && <div className="success-alert" role="status">{message}</div>}

        <form className="login-form" onSubmit={submit}>
          {mode === "signup" && (
            <>
              <label className="field">
                <span>Nom complet</span>
                <input
                  autoComplete="name"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  minLength="2"
                  required
                />
              </label>
              <label className="field">
                <span>Email</span>
                <input
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </label>
            </>
          )}
          {mode === "forgot" && (
            <label className="field">
              <span>Email du compte</span>
              <input
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>
          )}
          {(mode === "login" || mode === "signup") && <label className="field">
            <span>{mode === "login" ? "Nom d'utilisateur ou email" : "Nom d'utilisateur"}</span>
            <input
              autoComplete="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              minLength={mode === "signup" ? 3 : 1}
            />
          </label>}
          {mode !== "forgot" && <label className="field">
            <span>Mot de passe</span>
            <input
              type="password"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              minLength={mode === "login" ? 1 : 8}
            />
          </label>}
          {(mode === "signup" || mode === "reset") && (
            <label className="field">
              <span>Confirmer le mot de passe</span>
              <input
                type="password"
                autoComplete="new-password"
                value={passwordConfirmation}
                onChange={(event) => setPasswordConfirmation(event.target.value)}
                minLength="8"
                required
              />
            </label>
          )}
          <button className="button primary login-button" disabled={loading}>
            {loading
              ? "Traitement..."
              : mode === "login" ? "Se connecter"
              : mode === "signup" ? "Creer mon compte"
              : mode === "forgot" ? "Envoyer le lien"
              : "Modifier le mot de passe"}
          </button>
          {mode === "login" && (
            <button type="button" className="auth-link" onClick={() => changeMode("forgot")}>
              Mot de passe oublie ?
            </button>
          )}
          {(mode === "forgot" || mode === "reset") && (
            <button type="button" className="auth-link" onClick={() => changeMode("login")}>
              Retour a la connexion
            </button>
          )}
        </form>
      </section>
    </main>
  );
}
