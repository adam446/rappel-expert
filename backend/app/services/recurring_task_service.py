from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.recurring_task import RecurringTask
from app.models.reminder import Reminder
from app.schemas.recurring_task import RecurringTaskCreate, RecurringTaskUpdate
from app.services.reminder_generator import generate_reminders


def get_recurring_tasks(db: Session, user_id: int | None) -> list[RecurringTask]:
    query = db.query(RecurringTask)
    if user_id is not None:
        query = query.filter(RecurringTask.user_id == user_id)
    return query.order_by(RecurringTask.created_at.desc()).all()


def get_recurring_task(
    db: Session, task_id: int, user_id: int | None
) -> RecurringTask:
    query = db.query(RecurringTask).filter(RecurringTask.id == task_id)
    if user_id is not None:
        query = query.filter(RecurringTask.user_id == user_id)
    task = query.first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tache recurrente introuvable.")
    return task


def create_recurring_task(
    db: Session, data: RecurringTaskCreate, user_id: int
) -> RecurringTask:
    task = RecurringTask(user_id=user_id, **data.model_dump())
    db.add(task)
    db.flush()
    if task.status == "active":
        generate_reminders(db, task)
    db.commit()
    db.refresh(task)
    return task


def update_recurring_task(
    db: Session, task_id: int, data: RecurringTaskUpdate, user_id: int | None
) -> RecurringTask:
    task = get_recurring_task(db, task_id, user_id)
    values = data.model_dump(exclude_unset=True)

    for field, value in values.items():
        setattr(task, field, value)

    if task.start_date > task.end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La date de debut doit preceder la date de fin.",
        )

    completed = (
        db.query(Reminder)
        .filter(
            Reminder.recurring_task_id == task.id,
            Reminder.status == "completed",
        )
        .all()
    )
    if task.status == "active":
        completed_dates = {reminder.due_date for reminder in completed}
        db.query(Reminder).filter(
            Reminder.recurring_task_id == task.id,
            Reminder.status != "completed",
        ).delete(synchronize_session=False)
        db.flush()
        generate_reminders(db, task, completed_dates)
    else:
        target_status = "cancelled" if task.status == "cancelled" else "archived"
        reminders = (
            db.query(Reminder)
            .filter(
                Reminder.recurring_task_id == task.id,
                Reminder.status != "completed",
            )
            .all()
        )
        for reminder in reminders:
            reminder.status = target_status
            reminder.expert_state = target_status
            reminder.color = "gray"

    db.commit()
    db.refresh(task)
    return task


def archive_recurring_task(
    db: Session, task_id: int, user_id: int | None
) -> RecurringTask:
    task = get_recurring_task(db, task_id, user_id)
    task.status = "archived"
    reminders = db.query(Reminder).filter(Reminder.recurring_task_id == task.id).all()
    for reminder in reminders:
        reminder.status = "archived"
        reminder.expert_state = "archived"
        reminder.color = "gray"
    db.commit()
    db.refresh(task)
    return task
