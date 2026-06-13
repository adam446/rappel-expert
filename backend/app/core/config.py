import os


# Docker fournit DATABASE_URL au conteneur backend.
# La valeur par defaut permet de garder la meme configuration avec Docker Compose.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://smart_user:smart_password@db:5432/smart_reminders",
)
