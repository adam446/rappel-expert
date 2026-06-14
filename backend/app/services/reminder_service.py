from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.reminder import Reminder
from app.models.recurring_task import RecurringTask
from app.schemas.reminder import ReminderUpdate
from app.services.expert_rules_service import (
    apply_rules_to_all_reminders,
    apply_rules_to_reminder,
)


def reminder_query(db: Session, user_id: int | None):
    query = db.query(Reminder).join(RecurringTask)
    if user_id is not None:
        query = query.filter(RecurringTask.user_id == user_id)
    return query


def get_reminders(db: Session, user_id: int | None) -> list[Reminder]:
    apply_rules_to_all_reminders(db, user_id=user_id)
    return reminder_query(db, user_id).order_by(Reminder.due_date).all()


def get_reminder(db: Session, reminder_id: int, user_id: int | None) -> Reminder:
    reminder = reminder_query(db, user_id).filter(Reminder.id == reminder_id).first()
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def get_overdue_reminders(db: Session, user_id: int | None) -> list[Reminder]:
    apply_rules_to_all_reminders(db, user_id=user_id)
    return (
        reminder_query(db, user_id)
        .filter(Reminder.expert_state == "overdue")
        .order_by(Reminder.due_date)
        .all()
    )


def get_upcoming_reminders(db: Session, user_id: int | None) -> list[Reminder]:
    apply_rules_to_all_reminders(db, user_id=user_id)
    today = date.today()
    return (
        reminder_query(db, user_id)
        .filter(
            Reminder.due_date >= today,
            Reminder.due_date <= today + timedelta(days=7),
            Reminder.expert_state == "urgent",
        )
        .order_by(Reminder.due_date)
        .all()
    )


def update_reminder(
    db: Session, reminder_id: int, data: ReminderUpdate, user_id: int | None
) -> Reminder:
    reminder = reminder_query(db, user_id).filter(Reminder.id == reminder_id).first()
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def complete_reminder(
    db: Session, reminder_id: int, user_id: int | None
) -> Reminder:
    reminder = reminder_query(db, user_id).filter(Reminder.id == reminder_id).first()
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    reminder.status = "completed"
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, reminder_id: int, user_id: int | None) -> None:
    reminder = reminder_query(db, user_id).filter(Reminder.id == reminder_id).first()
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    db.delete(reminder)
    db.commit()
