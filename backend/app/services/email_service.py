import os
import smtplib
import ssl
from email.message import EmailMessage


def send_password_reset_email(recipient: str, full_name: str, token: str) -> None:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    # Google affiche les mots de passe d'application en groupes espaces.
    smtp_password = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)
    from_name = os.getenv("SMTP_FROM_NAME", "Rappel Expert")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

    if not smtp_host or not from_email:
        raise RuntimeError("La configuration SMTP est incomplete.")

    reset_url = f"{frontend_url}/?reset_token={token}"
    message = EmailMessage()
    message["Subject"] = "Reinitialisation de votre mot de passe"
    message["From"] = f"{from_name} <{from_email}>"
    message["To"] = recipient
    message.set_content(
        f"""Bonjour {full_name},

Une demande de reinitialisation de mot de passe a ete effectuee.

Utilisez ce lien dans les 30 prochaines minutes :
{reset_url}

Si vous n'etes pas a l'origine de cette demande, ignorez ce message.
"""
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
        if use_tls:
            server.starttls(context=context)
        if smtp_username:
            server.login(smtp_username, smtp_password)
        server.send_message(message)
