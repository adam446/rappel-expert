from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.recurring_task import (
    RecurringTaskCreate,
    RecurringTaskRead,
    RecurringTaskUpdate,
)
from app.services import recurring_task_service


router = APIRouter(prefix="/recurring-tasks", tags=["Recurring tasks"])


@router.get("", response_model=list[RecurringTaskRead])
def list_recurring_tasks(db: Session = Depends(get_db)):
    return recurring_task_service.get_recurring_tasks(db)


@router.get("/{task_id}", response_model=RecurringTaskRead)
def read_recurring_task(task_id: int, db: Session = Depends(get_db)):
    return recurring_task_service.get_recurring_task(db, task_id)


@router.post("", response_model=RecurringTaskRead, status_code=status.HTTP_201_CREATED)
def create_recurring_task(
    data: RecurringTaskCreate, db: Session = Depends(get_db)
):
    return recurring_task_service.create_recurring_task(db, data)


@router.put("/{task_id}", response_model=RecurringTaskRead)
def update_recurring_task(
    task_id: int, data: RecurringTaskUpdate, db: Session = Depends(get_db)
):
    return recurring_task_service.update_recurring_task(db, task_id, data)


@router.delete("/{task_id}", response_model=RecurringTaskRead)
def archive_recurring_task(task_id: int, db: Session = Depends(get_db)):
    return recurring_task_service.archive_recurring_task(db, task_id)
