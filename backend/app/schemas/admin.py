from datetime import datetime

from pydantic import BaseModel


class AdminStats(BaseModel):
    users: int
    active_users: int
    recurring_tasks: int
    reminders: int


class AdminUserRead(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    task_count: int
    reminder_count: int


class AdminDashboardRead(BaseModel):
    stats: AdminStats
    users: list[AdminUserRead]
