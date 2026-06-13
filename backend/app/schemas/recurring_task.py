from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


Frequency = Literal["monthly", "weekly"]
RecurringStatus = Literal["active", "cancelled", "archived"]


class RecurringTaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    start_date: date
    end_date: date
    day_of_month: int = Field(ge=1, le=31)
    frequency: Frequency = "monthly"
    status: RecurringStatus = "active"

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("La date de debut doit preceder la date de fin.")
        return self


class RecurringTaskCreate(RecurringTaskBase):
    pass


class RecurringTaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    start_date: date | None = None
    end_date: date | None = None
    day_of_month: int | None = Field(default=None, ge=1, le=31)
    frequency: Frequency | None = None
    status: RecurringStatus | None = None


class RecurringTaskRead(RecurringTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
