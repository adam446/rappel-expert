import os
import hashlib
import secrets
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.password_reset_token import PasswordResetToken


def authenticate(db: Session, identifier: str, password: str) -> User | None:
    normalized_identifier = identifier.strip().lower()
    user = (
        db.query(User)
        .filter(
            or_(
                User.username == normalized_identifier,
                User.email == normalized_identifier,
            )
        )
        .first()
    )
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        return None
    return user


def create_user(
    db: Session,
    full_name: str,
    username: str,
    email: str,
    password: str,
) -> User:
    normalized_username = username.strip().lower()
    normalized_email = email.strip().lower()
    duplicate = (
        db.query(User)
        .filter(
            or_(
                User.username == normalized_username,
                User.email == normalized_email,
            )
        )
        .first()
    )
    if duplicate:
        raise ValueError("Ce nom d'utilisateur ou cet email est deja utilise.")

    user = User(
        full_name=" ".join(full_name.split()),
        username=normalized_username,
        email=normalized_email,
        password_hash=hash_password(password),
        is_admin=False,
        is_active=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise ValueError(
            "Ce nom d'utilisateur ou cet email est deja utilise."
        ) from error
    db.refresh(user)
    return user


def ensure_admin_user(db: Session) -> None:
    full_name = os.getenv("ADMIN_FULL_NAME", "Administrateur")
    username = os.getenv("ADMIN_USERNAME", "admin").strip().lower()
    email = os.getenv("ADMIN_EMAIL", "admin@example.com").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return

    db.add(
        User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=hash_password(password),
            is_admin=True,
            is_active=True,
        )
    )
    db.commit()


def create_password_reset_token(db: Session, email: str) -> tuple[User, str] | None:
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not user.is_active:
        return None

    now = datetime.utcnow()
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None),
    ).update({PasswordResetToken.used_at: now}, synchronize_session=False)

    raw_token = secrets.token_urlsafe(48)
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hashlib.sha256(raw_token.encode()).hexdigest(),
            expires_at=now + timedelta(minutes=30),
        )
    )
    db.commit()
    return user, raw_token


def reset_password(db: Session, token: str, password: str) -> bool:
    now = datetime.utcnow()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    reset_token = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at >= now,
        )
        .first()
    )
    if not reset_token:
        return False

    reset_token.user.password_hash = hash_password(password)
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == reset_token.user_id,
        PasswordResetToken.used_at.is_(None),
    ).update({PasswordResetToken.used_at: now}, synchronize_session=False)
    db.commit()
    return True
