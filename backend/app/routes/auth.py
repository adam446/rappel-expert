import logging
import smtplib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordRequest,
    SignupRequest,
    UserRead,
)
from app.services.auth_service import (
    authenticate,
    create_password_reset_token,
    create_user,
    reset_password,
)
from app.services.email_service import send_password_reset_email


router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return LoginResponse(
        access_token=create_access_token(user.id, user.username),
        user=user,
    )


@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db,
            data.full_name,
            data.username,
            data.email,
            data.password,
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return LoginResponse(
        access_token=create_access_token(user.id, user.username),
        user=user,
    )


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    reset_data = create_password_reset_token(db, data.email)
    if reset_data:
        user, token = reset_data
        try:
            send_password_reset_email(user.email, user.full_name, token)
        except (OSError, RuntimeError, smtplib.SMTPException):
            logger.exception("Echec de l'envoi du courriel de reinitialisation")
    return MessageResponse(
        message="Si ce courriel existe, un lien de reinitialisation a ete envoye."
    )


@router.post("/reset-password", response_model=MessageResponse)
def change_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not reset_password(db, data.token, data.password):
        raise HTTPException(
            status_code=400,
            detail="Le lien de reinitialisation est invalide ou expire.",
        )
    return MessageResponse(message="Votre mot de passe a ete modifie.")


@router.get("/me", response_model=UserRead)
def current_user(user: User = Depends(get_current_user)):
    return user
