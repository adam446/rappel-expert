from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.reminder import ReminderRead, ReminderUpdate
from app.services import reminder_service


router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.get("", response_model=list[ReminderRead])
def list_reminders(db: Session = Depends(get_db)):
    return reminder_service.get_reminders(db)


@router.get("/overdue", response_model=list[ReminderRead])
def list_overdue_reminders(db: Session = Depends(get_db)):
    return reminder_service.get_overdue_reminders(db)


@router.get("/upcoming", response_model=list[ReminderRead])
def list_upcoming_reminders(db: Session = Depends(get_db)):
    return reminder_service.get_upcoming_reminders(db)


@router.get("/{reminder_id}", response_model=ReminderRead)
def read_reminder(reminder_id: int, db: Session = Depends(get_db)):
    return reminder_service.get_reminder(db, reminder_id)


@router.put("/{reminder_id}", response_model=ReminderRead)
def update_reminder(
    reminder_id: int, data: ReminderUpdate, db: Session = Depends(get_db)
):
    return reminder_service.update_reminder(db, reminder_id, data)


@router.put("/{reminder_id}/complete", response_model=ReminderRead)
def complete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    return reminder_service.complete_reminder(db, reminder_id)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    reminder_service.delete_reminder(db, reminder_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
