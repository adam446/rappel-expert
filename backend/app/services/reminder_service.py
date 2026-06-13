from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.reminder import Reminder
from app.schemas.reminder import ReminderUpdate
from app.services.expert_rules_service import (
    apply_rules_to_all_reminders,
    apply_rules_to_reminder,
)


def get_reminders(db: Session) -> list[Reminder]:
    apply_rules_to_all_reminders(db)
    return db.query(Reminder).order_by(Reminder.due_date).all()


def get_reminder(db: Session, reminder_id: int) -> Reminder:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def get_overdue_reminders(db: Session) -> list[Reminder]:
    apply_rules_to_all_reminders(db)
    return (
        db.query(Reminder)
        .filter(Reminder.expert_state == "overdue")
        .order_by(Reminder.due_date)
        .all()
    )


def get_upcoming_reminders(db: Session) -> list[Reminder]:
    apply_rules_to_all_reminders(db)
    today = date.today()
    return (
        db.query(Reminder)
        .filter(
            Reminder.due_date >= today,
            Reminder.due_date <= today + timedelta(days=7),
            Reminder.expert_state == "urgent",
        )
        .order_by(Reminder.due_date)
        .all()
    )


def update_reminder(
    db: Session, reminder_id: int, data: ReminderUpdate
) -> Reminder:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def complete_reminder(db: Session, reminder_id: int) -> Reminder:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    reminder.status = "completed"
    apply_rules_to_reminder(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, reminder_id: int) -> None:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Rappel introuvable.")
    db.delete(reminder)
    db.commit()
