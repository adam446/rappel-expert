from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import expert_rules_router, recurring_tasks_router, reminders_router


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

app.include_router(recurring_tasks_router)
app.include_router(reminders_router)
app.include_router(expert_rules_router)


@app.get("/")
def root():
    return {"message": "API du systeme expert operationnelle"}


@app.get("/health")
def health():
    return {"status": "ok"}
