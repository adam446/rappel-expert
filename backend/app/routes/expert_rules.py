from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.reminder import ReminderRead
from app.services.expert_rules_service import apply_rules_to_all_reminders


router = APIRouter(prefix="/expert-rules", tags=["Expert rules"])


@router.post("/apply", response_model=list[ReminderRead])
def apply_expert_rules(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return apply_rules_to_all_reminders(
        db, user_id=None if user.is_admin else user.id
    )
