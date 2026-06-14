import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.core.database import Base, SessionLocal, engine
from app.models import User  # noqa: F401 - enregistre le modele dans les metadonnees
from app.routes import (
    admin_router,
    auth_router,
    expert_rules_router,
    recurring_tasks_router,
    reminders_router,
)
from app.services.auth_service import ensure_admin_user


app = FastAPI(
    title="Systeme expert de gestion des taches recurrentes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(recurring_tasks_router)
app.include_router(reminders_router)
app.include_router(expert_rules_router)


@app.on_event("startup")
def initialize_database():
    Base.metadata.create_all(bind=engine)
    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    if "full_name" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN full_name VARCHAR(150)")
            )
            connection.execute(
                text("UPDATE users SET full_name = username WHERE full_name IS NULL")
            )
            connection.execute(
                text("ALTER TABLE users ALTER COLUMN full_name SET NOT NULL")
            )
    if "email" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR(255)"))
            connection.execute(
                text(
                    """
                    UPDATE users
                    SET email = CASE
                        WHEN username = :admin_username THEN :admin_email
                        ELSE username || '@local.invalid'
                    END
                    WHERE email IS NULL
                    """
                ),
                {
                    "admin_username": os.getenv("ADMIN_USERNAME", "admin").strip().lower(),
                    "admin_email": os.getenv("ADMIN_EMAIL", "admin@example.com").strip().lower(),
                },
            )
            connection.execute(text("ALTER TABLE users ALTER COLUMN email SET NOT NULL"))
            connection.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)")
            )
    task_columns = {
        column["name"] for column in inspect(engine).get_columns("recurring_tasks")
    }
    if "user_id" not in task_columns:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    ALTER TABLE recurring_tasks
                    ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
                    """
                )
            )
            connection.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_recurring_tasks_user_id "
                    "ON recurring_tasks (user_id)"
                )
            )
    with SessionLocal() as db:
        ensure_admin_user(db)
        admin = db.query(User).filter(User.is_admin.is_(True)).order_by(User.id).first()
        if admin:
            db.execute(
                text(
                    "UPDATE recurring_tasks SET user_id = :admin_id "
                    "WHERE user_id IS NULL"
                ),
                {"admin_id": admin.id},
            )
            db.commit()
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE recurring_tasks "
                        "ALTER COLUMN user_id SET NOT NULL"
                    )
                )


@app.get("/")
def root():
    return {"message": "API du systeme expert operationnelle"}


@app.get("/health")
def health():
    return {"status": "ok"}
