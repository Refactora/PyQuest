from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.services.xp_service import get_title_for_level

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

TOP_LIMIT = 100


@router.get("", summary="Глобальний лідерборд (за total_xp)")
def get_leaderboard(
    limit: int = Query(default=50, ge=1, le=TOP_LIMIT),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    top_users = (
        db.query(User)
        .order_by(desc(User.total_xp))
        .limit(limit)
        .all()
    )

    result = []
    for rank, user in enumerate(top_users, start=1):
        result.append({
            "rank": rank,
            "user_id": user.id,
            "username": user.username,
            "avatar_id": user.avatar_id,
            "level": user.level,
            "title": get_title_for_level(user.level),
            "total_xp": user.total_xp,
            "is_me": user.id == current_user.id,
        })

    # Знайти позицію поточного юзера якщо він не в топі
    my_rank = None
    my_entry = None
    if not any(u["is_me"] for u in result):
        all_users = db.query(User).order_by(desc(User.total_xp)).all()
        for rank, user in enumerate(all_users, start=1):
            if user.id == current_user.id:
                my_rank = rank
                my_entry = {
                    "rank": rank,
                    "user_id": user.id,
                    "username": user.username,
                    "avatar_id": user.avatar_id,
                    "level": user.level,
                    "title": get_title_for_level(user.level),
                    "total_xp": user.total_xp,
                    "is_me": True,
                }
                break

    return {
        "leaderboard": result,
        "my_rank": my_rank or (next((i + 1 for i, u in enumerate(result) if u["is_me"]), None)),
        "my_entry": my_entry,
        "total_players": db.query(User).count(),
    }
