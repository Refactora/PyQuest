from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MeResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалідний або прострочений токен",
        )
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено",
        )
    return user


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
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})
    return AuthResponse(user=UserResponse.model_validate(user), access_token=token)


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")

    token = create_access_token({"sub": user.id})
    return AuthResponse(user=UserResponse.model_validate(user), access_token=token)


@router.get("/me", response_model=MeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return MeResponse(user=UserResponse.model_validate(current_user))