from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.recurring_task import RecurringTask
from app.models.reminder import Reminder
from app.models.user import User


def get_admin_dashboard(db: Session) -> dict:
    task_counts = dict(
        db.query(RecurringTask.user_id, func.count(RecurringTask.id))
        .group_by(RecurringTask.user_id)
        .all()
    )
    reminder_counts = dict(
        db.query(RecurringTask.user_id, func.count(Reminder.id))
        .join(Reminder, Reminder.recurring_task_id == RecurringTask.id)
        .group_by(RecurringTask.user_id)
        .all()
    )
    users = db.query(User).order_by(User.created_at.desc()).all()

    return {
        "stats": {
            "users": len(users),
            "active_users": sum(user.is_active for user in users),
            "recurring_tasks": db.query(func.count(RecurringTask.id)).scalar() or 0,
            "reminders": db.query(func.count(Reminder.id)).scalar() or 0,
        },
        "users": [
            {
                "id": user.id,
                "full_name": user.full_name,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "task_count": task_counts.get(user.id, 0),
                "reminder_count": reminder_counts.get(user.id, 0),
            }
            for user in users
        ],
    }
