from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"
    __table_args__ = (
        UniqueConstraint(
            "recurring_task_id",
            "due_date",
            name="uq_reminders_recurring_task_due_date",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    recurring_task_id = Column(
        Integer,
        ForeignKey("recurring_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(10, 2), nullable=True)
    due_date = Column(Date, nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending")
    expert_state = Column(String(50), nullable=False, default="normal", index=True)
    color = Column(String(50), nullable=False, default="blue")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recurring_task = relationship("RecurringTask", back_populates="reminders")
