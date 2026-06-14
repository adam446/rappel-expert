from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.reminder import Reminder
from app.models.recurring_task import RecurringTask


def apply_rules_to_reminder(reminder: Reminder, today: date | None = None) -> Reminder:
    current_date = today or date.today()

    if reminder.status == "completed":
        reminder.expert_state = "completed"
        reminder.color = "green"
    elif reminder.status == "cancelled":
        reminder.expert_state = "cancelled"
        reminder.color = "gray"
    elif reminder.status == "archived":
        reminder.expert_state = "archived"
        reminder.color = "gray"
    elif reminder.due_date < current_date:
        reminder.expert_state = "overdue"
        reminder.color = "red"
    elif reminder.due_date <= current_date + timedelta(days=7):
        reminder.expert_state = "urgent"
        reminder.color = "orange"
    else:
        reminder.expert_state = "normal"
        reminder.color = "blue"

    return reminder


def apply_rules_to_all_reminders(
    db: Session, today: date | None = None, user_id: int | None = None
) -> list[Reminder]:
    query = db.query(Reminder).join(RecurringTask)
    if user_id is not None:
        query = query.filter(RecurringTask.user_id == user_id)
    reminders = query.all()
    for reminder in reminders:
        apply_rules_to_reminder(reminder, today)
    db.commit()
    for reminder in reminders:
        db.refresh(reminder)
    return reminders
