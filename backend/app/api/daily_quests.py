from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.services.daily_quest_service import get_or_create_daily_quests, format_quest

router = APIRouter(prefix="/daily-quests", tags=["Daily Quests"])


@router.get("", summary="Отримати щоденні квести")
def get_daily_quests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quests = get_or_create_daily_quests(current_user, db)
    completed = sum(1 for q in quests if q.is_completed)
    return {
        "quests": [format_quest(q) for q in quests],
        "completed": completed,
        "total": len(quests),
        "all_done": completed == len(quests),
    }
