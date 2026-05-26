from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.location import Location, Question
from app.models.progress import UserLocationProgress

router = APIRouter(prefix="/locations", tags=["Locations"])


def _get_progress(user_id: str, location_id: int, db: Session):
    return db.query(UserLocationProgress).filter(
        UserLocationProgress.user_id == user_id,
        UserLocationProgress.location_id == location_id,
    ).first()


def _fmt_location(loc: Location, p) -> dict:
    return {
        "id": loc.id, "slug": loc.slug, "name": loc.name,
        "description": loc.description, "topic": loc.topic,
        "order_index": loc.order_index, "boss_name": loc.boss_name,
        "boss_sprite_id": loc.boss_sprite_id, "background_id": loc.background_id,
        "enemy_sprite_id": loc.enemy_sprite_id, "color_theme": loc.color_theme,
        "progress": {
            "status": p.status if p else "locked",
            "quiz_completed": p.quiz_completed if p else False,
            "boss_defeated": p.boss_defeated if p else False,
            "best_quiz_score": p.best_quiz_score if p else 0,
            "quiz_attempts": p.quiz_attempts if p else 0,
            "boss_attempts": p.boss_attempts if p else 0,
            "no_death_run": p.no_death_run if p else False,
            "first_try_boss": p.first_try_boss if p else False,
            "completed_at": p.completed_at.isoformat() if p and p.completed_at else None,
        },
    }


@router.get("")
def get_locations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    locations = db.query(Location).filter(Location.is_active == True).order_by(Location.order_index).all()
    result = [_fmt_location(loc, _get_progress(current_user.id, loc.id, db)) for loc in locations]
    return {"locations": result, "total": len(result)}


@router.get("/{slug}")
def get_location(slug: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    loc = db.query(Location).filter(Location.slug == slug, Location.is_active == True).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")

    p = _get_progress(current_user.id, loc.id, db)
    questions_count = db.query(Question).filter(Question.location_id == loc.id, Question.is_active == True).count()

    boss = loc.boss_challenge
    boss_data = None
    if boss:
        boss_data = {
            "id": boss.id, "title": boss.title, "story_text": boss.story_text,
            "task_text": boss.task_text, "function_signature": boss.function_signature,
            "starter_code": boss.starter_code, "hints_count": len(boss.hints),
            "boss_hp": boss.boss_hp, "time_limit_sec": boss.time_limit_sec,
            "test_cases_visible": [
                {"input": tc["input"], "expected_output": tc["expected_output"], "description": tc.get("description", "")}
                for tc in boss.test_cases if not tc.get("is_hidden", False)
            ],
        }

    return {**_fmt_location(loc, p), "boss": boss_data, "questions_count": questions_count}


@router.post("/{slug}/enter")
def enter_location(slug: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Позначає локацію як 'in_progress' при вході."""
    loc = db.query(Location).filter(Location.slug == slug, Location.is_active == True).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")

    p = _get_progress(current_user.id, loc.id, db)
    if not p or p.status == "locked":
        raise HTTPException(status_code=403, detail="Локація заблокована")

    if p.status == "available":
        p.status = "in_progress"
        db.add(p)
        db.commit()

    return {"status": p.status, "location_id": loc.id, "slug": loc.slug}
