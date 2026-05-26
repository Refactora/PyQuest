import re
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    avatar_id: int = Field(default=1, ge=1, le=4)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Ім'я може містити лише літери, цифри та _")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль має містити хоча б одну літеру")
        if not re.search(r"\d", v):
            raise ValueError("Пароль має містити хоча б одну цифру")
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    avatar_id: int
    level: int
    xp: int
    xp_to_next: int
    total_xp: int
    hp_max: int
    streak_days: int
    model_config = {"from_attributes": True}

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class MeResponse(BaseModel):
    user: UserResponse
