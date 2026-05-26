from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import (
    create_access_token, create_refresh_token,
    decode_token, hash_password, verify_password,
)
from app.models.user import User
from app.models.location import Location
from app.models.progress import UserLocationProgress
from app.schemas.auth import (
    AuthResponse, LoginRequest, MeResponse,
    RegisterRequest, UserResponse, RefreshRequest,
)
from app.services.xp_service import xp_for_level

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials if credentials else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен відсутній")
    payload = decode_token(token, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалідний або прострочений токен")
    user = db.query(User).filter(User.id == payload.get("sub"), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Користувача не знайдено")
    return user


def _init_location_progress(user: User, db: Session):
    locations = db.query(Location).filter(Location.is_active == True).order_by(Location.order_index).all()
    for i, loc in enumerate(locations):
        db.add(UserLocationProgress(
            user_id=user.id,
            location_id=loc.id,
            status="available" if i == 0 else "locked",
        ))


def _build_auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=create_access_token({"sub": user.id}),
        refresh_token=create_refresh_token({"sub": user.id}),
    )


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=409, detail="Цей email вже зареєстрований")
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=409, detail="Це ім'я вже зайнято")

    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        avatar_id=request.avatar_id,
        xp_to_next=xp_for_level(2) - xp_for_level(1),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _init_location_progress(user, db)
    db.commit()
    return _build_auth_response(user)


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email, User.is_active == True).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")
    return _build_auth_response(user)


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Невалідний refresh token")
    user = db.query(User).filter(User.id == payload.get("sub"), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    return _build_auth_response(user)


@router.post("/logout")
def logout():
    # Клієнт видаляє токени зі свого сховища
    return {"message": "Успішно вийшли з системи"}


@router.get("/me", response_model=MeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return MeResponse(user=UserResponse.model_validate(current_user))
