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

class AbandonRequest(BaseModel):
    session_id: str


@router.post("/start")
def start_quiz(req: StartQuizRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return quiz_service.start_quiz(current_user, req.location_slug, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/answer")
def answer_question(req: AnswerRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.selected_option not in ("a", "b", "c", "d"):
        raise HTTPException(status_code=422, detail="Варіант має бути: a, b, c або d")
    try:
        return quiz_service.answer_question(current_user, req.session_id, req.question_id, req.selected_option, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/abandon")
def abandon_quiz(req: AbandonRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return quiz_service.abandon_quiz(current_user, req.session_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/session/{session_id}")
def get_session(session_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return quiz_service.get_current_question(current_user, session_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
