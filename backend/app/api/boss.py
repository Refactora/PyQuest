from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.location import Location
from app.models.boss_challenge import BossChallenge
from app.models.progress import BossSession, UserLocationProgress
from app.services.xp_service import add_xp, unlock_achievement, check_and_award_achievements
from app.services.judge0_service import run_all_tests
from app.services.claude_service import get_ai_hint
from app.services.daily_quest_service import update_quest_progress

router = APIRouter(prefix="/boss", tags=["Boss Fight"])

XP_BOSS_WIN = 150
XP_FIRST_TRY_BONUS = 50
XP_NO_HINTS_BONUS = 30


class StartBossRequest(BaseModel):
    location_slug: str

class SubmitCodeRequest(BaseModel):
    session_id: str
    code: str

class UseHintRequest(BaseModel):
    session_id: str
    hint_order: int  # 1 | 2 | 3

class AiHintRequest(BaseModel):
    session_id: str
    code: str


def _get_progress(user_id: str, location_id: int, db: Session):
    return db.query(UserLocationProgress).filter(
        UserLocationProgress.user_id == user_id,
        UserLocationProgress.location_id == location_id,
    ).first()


@router.post("/start")
def start_boss(req: StartBossRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.slug == req.location_slug, Location.is_active == True).first()
    if not location:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")

    progress = _get_progress(current_user.id, location.id, db)
    if not progress or not progress.quiz_completed:
        raise HTTPException(status_code=403, detail="Спочатку пройди квіз цієї локації")

    challenge = db.query(BossChallenge).filter(BossChallenge.location_id == location.id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Задачу для боса не знайдено")

    db.query(BossSession).filter(
        BossSession.user_id == current_user.id, BossSession.is_active == True
    ).update({"is_active": False, "completed_at": datetime.now(timezone.utc)})

    session = BossSession(
        user_id=current_user.id,
        challenge_id=challenge.id,
        hero_hp=current_user.hp_max,
        boss_hp=challenge.boss_hp,
        is_active=True,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    visible_tests = [
        {"input": tc["input"], "expected_output": tc["expected_output"], "description": tc.get("description", "")}
        for tc in challenge.test_cases if not tc.get("is_hidden", False)
    ]

    return {
        "session_id": session.id,
        "boss": {"name": location.boss_name, "hp": challenge.boss_hp, "sprite_id": location.boss_sprite_id},
        "challenge": {
            "id": challenge.id,
            "title": challenge.title,
            "story_text": challenge.story_text,
            "task_text": challenge.task_text,
            "function_signature": challenge.function_signature,
            "starter_code": challenge.starter_code,
            "visible_test_cases": visible_tests,
        },
        "hero_hp": session.hero_hp,
        "hints_available": len(challenge.hints),
        "hints_used": 0,
    }


@router.post("/submit")
async def submit_code(req: SubmitCodeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(BossSession).filter(
        BossSession.id == req.session_id,
        BossSession.user_id == current_user.id,
        BossSession.is_active == True,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сесію не знайдено або вже завершена")

    challenge = db.query(BossChallenge).filter(BossChallenge.id == session.challenge_id).first()
    test_results = await run_all_tests(req.code, challenge)

    passed_count = sum(1 for r in test_results if r["passed"])
    total_count = len(test_results)
    attempt_num = len(session.submissions) + 1

    submissions = list(session.submissions)
    submissions.append({
        "attempt": attempt_num, "code": req.code,
        "test_results": test_results, "passed_count": passed_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    session.submissions = submissions

    boss_damage = passed_count * (challenge.boss_hp // total_count)
    session.boss_hp = max(0, session.boss_hp - boss_damage)
    if passed_count == 0:
        session.hero_hp -= 1

    new_achievements = []

    if session.boss_hp <= 0 or passed_count == total_count:
        session.boss_hp = 0
        session.is_won = True
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)

        bonus_xp = XP_BOSS_WIN
        first_try = attempt_num == 1
        no_hints = session.hints_used == 0

        add_xp(current_user, XP_BOSS_WIN, db)
        if first_try:
            add_xp(current_user, XP_FIRST_TRY_BONUS, db)
            bonus_xp += XP_FIRST_TRY_BONUS
            if unlock_achievement(current_user, "first_try", db):
                new_achievements.append("first_try")
        if no_hints:
            add_xp(current_user, XP_NO_HINTS_BONUS, db)
            bonus_xp += XP_NO_HINTS_BONUS
            if unlock_achievement(current_user, "no_hints", db):
                new_achievements.append("no_hints")

        location = db.query(Location).filter(Location.id == challenge.location_id).first()
        progress = _get_progress(current_user.id, location.id, db)
        if progress:
            progress.boss_defeated = True
            progress.boss_attempts += 1
            progress.status = "completed"
            progress.first_try_boss = first_try
            progress.hints_used += session.hints_used
            progress.completed_at = datetime.now(timezone.utc)
            db.add(progress)

            next_loc = db.query(Location).filter(
                Location.order_index == location.order_index + 1, Location.is_active == True
            ).first()
            if next_loc:
                next_prog = _get_progress(current_user.id, next_loc.id, db)
                if not next_prog:
                    db.add(UserLocationProgress(user_id=current_user.id, location_id=next_loc.id, status="available"))
                elif next_prog.status == "locked":
                    next_prog.status = "available"
                    db.add(next_prog)

        completed_quests = update_quest_progress(current_user, "defeat_boss", db)
        new_achievements += check_and_award_achievements(current_user, db)
        db.add(current_user)
        db.add(session)
        db.commit()

        return {
            "is_won": True, "boss_hp": 0, "hero_hp": session.hero_hp,
            "test_results": test_results, "passed_count": passed_count, "total_count": total_count,
            "xp_gained": bonus_xp, "first_try": first_try, "no_hints": no_hints,
            "new_achievements": new_achievements, "completed_quests": completed_quests,
        }

    if session.hero_hp <= 0:
        session.is_won = False
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)
        location = db.query(Location).filter(Location.id == challenge.location_id).first()
        progress = _get_progress(current_user.id, location.id, db)
        if progress:
            progress.boss_attempts += 1
            db.add(progress)
        db.add(session)
        db.commit()
        return {
            "is_won": False, "hero_died": True, "boss_hp": session.boss_hp, "hero_hp": 0,
            "test_results": test_results, "passed_count": passed_count, "total_count": total_count,
            "message": "Бос переміг! Спробуй ще раз.",
        }

    db.add(session)
    db.commit()
    return {
        "is_won": False, "hero_died": False, "boss_hp": session.boss_hp, "hero_hp": session.hero_hp,
        "test_results": test_results, "passed_count": passed_count, "total_count": total_count,
        "boss_damage": boss_damage, "attempt_number": attempt_num,
    }


@router.post("/hint")
def use_hint(req: UseHintRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(BossSession).filter(
        BossSession.id == req.session_id, BossSession.user_id == current_user.id, BossSession.is_active == True,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сесію не знайдено")

    challenge = db.query(BossChallenge).filter(BossChallenge.id == session.challenge_id).first()
    hint = next((h for h in challenge.hints if h["order"] == req.hint_order), None)
    if not hint:
        raise HTTPException(status_code=404, detail="Підказку не знайдено")
    if req.hint_order <= session.hints_used:
        raise HTTPException(status_code=400, detail="Цю підказку вже використано")

    hp_cost = hint["hp_cost"]
    session.hero_hp = max(0, session.hero_hp - hp_cost)
    session.hints_used = req.hint_order
    died = session.hero_hp <= 0
    if died:
        session.is_won = False
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()
    return {"hint_text": hint["text"], "hp_cost": hp_cost, "hero_hp": session.hero_hp, "hero_died": died, "hints_used": session.hints_used}


@router.post("/ai-hint")
async def ai_hint(req: AiHintRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """AI-підказка через Claude (не витрачає HP, але доступна тільки після 2+ спроб)."""
    session = db.query(BossSession).filter(
        BossSession.id == req.session_id, BossSession.user_id == current_user.id, BossSession.is_active == True,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сесію не знайдено")
    if len(session.submissions) < 2:
        raise HTTPException(status_code=400, detail="AI-підказка доступна після 2+ спроб")

    challenge = db.query(BossChallenge).filter(BossChallenge.id == session.challenge_id).first()
    last_results = session.submissions[-1].get("test_results", []) if session.submissions else []
    hint_level = min(len(session.submissions) - 1, 3)

    hint_text = await get_ai_hint(
        task_text=challenge.task_text,
        starter_code=challenge.starter_code,
        user_code=req.code,
        test_results=last_results,
        hint_level=hint_level,
    )
    return {"hint_text": hint_text, "hint_level": hint_level}
