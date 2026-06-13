from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ReminderStatus = Literal["pending", "completed", "cancelled", "archived"]


class ReminderUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    due_date: date | None = None
    status: ReminderStatus | None = None


class ReminderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recurring_task_id: int
    title: str
    description: str | None
    amount: Decimal | None
    due_date: date
    status: ReminderStatus
    expert_state: str
    color: str
    created_at: datetime
    updated_at: datetime
