from app.routes.admin import router as admin_router
from app.routes.auth import router as auth_router
from app.routes.expert_rules import router as expert_rules_router
from app.routes.recurring_tasks import router as recurring_tasks_router
from app.routes.reminders import router as reminders_router

__all__ = [
    "admin_router",
    "auth_router",
    "expert_rules_router",
    "recurring_tasks_router",
    "reminders_router",
]
