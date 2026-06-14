from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.admin import AdminDashboardRead
from app.services.admin_service import get_admin_dashboard


router = APIRouter(prefix="/admin", tags=["Administration"])


@router.get("/dashboard", response_model=AdminDashboardRead)
def dashboard(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return get_admin_dashboard(db)
