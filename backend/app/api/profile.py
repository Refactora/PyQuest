from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.progress import UserLocationProgress, UserAchievement, Achievement
from app.services.xp_service import get_title_for_level, update_streak

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", summary="Профіль поточного гравця")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    streak_result = update_streak(current_user, db)
    db.commit()

    progress_list = db.query(UserLocationProgress).filter(
        UserLocationProgress.user_id == current_user.id
    ).all()

    completed_locations = [p for p in progress_list if p.boss_defeated]
    quiz_total = sum(p.quiz_attempts for p in progress_list)
    boss_total = sum(p.boss_attempts for p in progress_list)

    uas = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()
    achievement_ids = [ua.achievement_id for ua in uas]
    achievements = db.query(Achievement).filter(Achievement.id.in_(achievement_ids)).all() if achievement_ids else []

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar_id": current_user.avatar_id,
        "level": current_user.level,
        "title": get_title_for_level(current_user.level),
        "xp": current_user.xp,
        "xp_to_next": current_user.xp_to_next,
        "total_xp": current_user.total_xp,
        "hp_max": current_user.hp_max,
        "streak_days": current_user.streak_days,
        "stats": {
            "locations_completed": len(completed_locations),
            "total_quiz_attempts": quiz_total,
            "total_boss_attempts": boss_total,
        },
        "completed_locations": [
            {
                "location_id": p.location_id,
                "quiz_score": p.best_quiz_score,
                "boss_attempts": p.boss_attempts,
                "first_try": p.first_try_boss,
                "no_death": p.no_death_run,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None,
            }
            for p in completed_locations
        ],
        "achievements": [
            {
                "id": a.id,
                "slug": a.slug,
                "name": a.name,
                "description": a.description,
                "icon_id": a.icon_id,
                "xp_reward": a.xp_reward,
            }
            for a in achievements
        ],
        "streak_bonus": streak_result.get("bonus_xp", 0),
    }


class UpdateAvatarRequest(BaseModel):
    avatar_id: int = Field(ge=1, le=4)


@router.patch("/avatar", summary="Змінити аватар")
def update_avatar(
    request: UpdateAvatarRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.avatar_id = request.avatar_id
    db.add(current_user)
    db.commit()
    return {"avatar_id": current_user.avatar_id, "message": "Аватар оновлено!"}
