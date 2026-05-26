from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, text
from datetime import date, timedelta

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.progress import BossSession
from app.services.xp_service import get_title_for_level

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


def _fmt_entry(rank: int, user: User, is_me: bool, xp_field: int) -> dict:
    return {
        "rank": rank, "user_id": user.id, "username": user.username,
        "avatar_id": user.avatar_id, "level": user.level,
        "title": get_title_for_level(user.level),
        "total_xp": xp_field, "is_me": is_me,
    }


@router.get("")
def get_leaderboard(
    period: str = Query(default="all", description="all | weekly"),
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if period == "weekly":
        since = date.today() - timedelta(days=7)
        # За тиждень рахуємо XP отримані через перемоги над босами
        # Спрощено: сортуємо по total_xp але фільтруємо активних за тиждень
        users = (
            db.query(User)
            .join(BossSession, BossSession.user_id == User.id)
            .filter(BossSession.completed_at >= since, BossSession.is_won == True)
            .group_by(User.id)
            .order_by(desc(func.count(BossSession.id)))
            .limit(limit)
            .all()
        )
        xp_map = {u.id: u.total_xp for u in users}
    else:
        users = db.query(User).filter(User.is_active == True).order_by(desc(User.total_xp)).limit(limit).all()
        xp_map = {u.id: u.total_xp for u in users}

    entries = [_fmt_entry(i + 1, u, u.id == current_user.id, xp_map[u.id]) for i, u in enumerate(users)]

    my_rank = None
    my_entry = None
    if not any(e["is_me"] for e in entries):
        all_users = db.query(User).filter(User.is_active == True).order_by(desc(User.total_xp)).all()
        for i, u in enumerate(all_users):
            if u.id == current_user.id:
                my_rank = i + 1
                my_entry = _fmt_entry(i + 1, u, True, u.total_xp)
                break

    return {
        "leaderboard": entries,
        "period": period,
        "my_rank": my_rank or next((i + 1 for i, e in enumerate(entries) if e["is_me"]), None),
        "my_entry": my_entry,
        "total_players": db.query(User).filter(User.is_active == True).count(),
    }
