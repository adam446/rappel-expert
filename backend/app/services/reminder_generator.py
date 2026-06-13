import calendar
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.recurring_task import RecurringTask
from app.models.reminder import Reminder
from app.services.expert_rules_service import apply_rules_to_reminder


def _monthly_dates(task: RecurringTask):
    year, month = task.start_date.year, task.start_date.month
    while date(year, month, 1) <= task.end_date:
        last_day = calendar.monthrange(year, month)[1]
        candidate = date(year, month, min(task.day_of_month, last_day))
        if task.start_date <= candidate <= task.end_date:
            yield candidate
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1


def _weekly_dates(task: RecurringTask):
    candidate = task.start_date
    while candidate <= task.end_date:
        yield candidate
        candidate += timedelta(days=7)


def generate_reminders(
    db: Session,
    task: RecurringTask,
    excluded_dates: set[date] | None = None,
) -> list[Reminder]:
    excluded_dates = excluded_dates or set()
    dates = _weekly_dates(task) if task.frequency == "weekly" else _monthly_dates(task)
    reminders = []

    for due_date in dates:
        if due_date in excluded_dates:
            continue
        reminder = Reminder(
            recurring_task_id=task.id,
            title=task.title,
            description=task.description,
            amount=task.amount,
            due_date=due_date,
            status="pending",
        )
        apply_rules_to_reminder(reminder)
        db.add(reminder)
        reminders.append(reminder)

    db.flush()
    return reminders
