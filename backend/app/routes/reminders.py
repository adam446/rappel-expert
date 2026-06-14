from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.reminder import ReminderRead, ReminderUpdate
from app.services import reminder_service


router = APIRouter(prefix="/reminders", tags=["Reminders"])


def user_scope(user: User) -> int | None:
    return None if user.is_admin else user.id


@router.get("", response_model=list[ReminderRead])
def list_reminders(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return reminder_service.get_reminders(db, user_scope(user))


@router.get("/overdue", response_model=list[ReminderRead])
def list_overdue_reminders(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return reminder_service.get_overdue_reminders(db, user_scope(user))


@router.get("/upcoming", response_model=list[ReminderRead])
def list_upcoming_reminders(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return reminder_service.get_upcoming_reminders(db, user_scope(user))


@router.get("/{reminder_id}", response_model=ReminderRead)
def read_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return reminder_service.get_reminder(db, reminder_id, user_scope(user))


@router.put("/{reminder_id}", response_model=ReminderRead)
def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return reminder_service.update_reminder(
        db, reminder_id, data, user_scope(user)
    )


@router.put("/{reminder_id}/complete", response_model=ReminderRead)
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return reminder_service.complete_reminder(db, reminder_id, user_scope(user))


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    reminder_service.delete_reminder(db, reminder_id, user_scope(user))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
