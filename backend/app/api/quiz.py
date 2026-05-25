from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.services import quiz_service

router = APIRouter(prefix="/quiz", tags=["Quiz"])


class StartQuizRequest(BaseModel):
    location_slug: str


class AnswerRequest(BaseModel):
    session_id: str
    question_id: int
    selected_option: str  # 'a' | 'b' | 'c' | 'd'


@router.post("/start", summary="Почати квіз у локації")
def start_quiz(
    request: StartQuizRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        result = quiz_service.start_quiz(current_user, request.location_slug, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/answer", summary="Відповісти на питання квізу")
def answer_question(
    request: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if request.selected_option not in ("a", "b", "c", "d"):
        raise HTTPException(status_code=422, detail="Варіант відповіді має бути: a, b, c або d")

    try:
        result = quiz_service.answer_question(
            current_user,
            request.session_id,
            request.question_id,
            request.selected_option,
            db,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/session/{session_id}", summary="Поточний стан сесії квізу")
def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return quiz_service.get_current_question(current_user, session_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
