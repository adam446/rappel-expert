from pydantic import BaseModel, Field, field_validator


USERNAME_PATTERN = r"^[A-Za-z0-9_.-]+$"
EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=200)


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=255, pattern=EMAIL_PATTERN)
    username: str = Field(min_length=3, max_length=100, pattern=USERNAME_PATTERN)
    password: str = Field(min_length=8, max_length=200)

    @field_validator("email", "username", mode="before")
    @classmethod
    def normalize_identity(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("full_name", mode="before")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        return " ".join(value.split())


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    is_admin: bool

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ForgotPasswordRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255, pattern=EMAIL_PATTERN)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=32, max_length=200)
    password: str = Field(min_length=8, max_length=200)


class MessageResponse(BaseModel):
    message: str
