from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.recurring_task import (
    RecurringTaskCreate,
    RecurringTaskRead,
    RecurringTaskUpdate,
)
from app.services import recurring_task_service


router = APIRouter(prefix="/recurring-tasks", tags=["Recurring tasks"])


def user_scope(user: User) -> int | None:
    return None if user.is_admin else user.id


@router.get("", response_model=list[RecurringTaskRead])
def list_recurring_tasks(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return recurring_task_service.get_recurring_tasks(db, user_scope(user))


@router.get("/{task_id}", response_model=RecurringTaskRead)
def read_recurring_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return recurring_task_service.get_recurring_task(db, task_id, user_scope(user))


@router.post("", response_model=RecurringTaskRead, status_code=status.HTTP_201_CREATED)
def create_recurring_task(
    data: RecurringTaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return recurring_task_service.create_recurring_task(db, data, user.id)


@router.put("/{task_id}", response_model=RecurringTaskRead)
def update_recurring_task(
    task_id: int,
    data: RecurringTaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return recurring_task_service.update_recurring_task(
        db, task_id, data, user_scope(user)
    )


@router.delete("/{task_id}", response_model=RecurringTaskRead)
def archive_recurring_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return recurring_task_service.archive_recurring_task(
        db, task_id, user_scope(user)
    )
