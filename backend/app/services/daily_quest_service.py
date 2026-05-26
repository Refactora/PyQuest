"""
Щоденні квести — генеруються щодня, прогрес оновлюється подіями.
"""
from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.progress import DailyQuest
from app.services.xp_service import add_xp

QUEST_DEFINITIONS = [
    {
        "quest_type": "answer_correct",
        "description": "Дай 5 правильних відповідей у квізах",
        "target_value": 5,
        "xp_reward": 30,
    },
    {
        "quest_type": "complete_quiz",
        "description": "Пройди 1 квіз до кінця",
        "target_value": 1,
        "xp_reward": 50,
    },
    {
        "quest_type": "defeat_boss",
        "description": "Переможи будь-якого боса",
        "target_value": 1,
        "xp_reward": 100,
    },
    {
        "quest_type": "answer_correct_10",
        "description": "Дай 10 правильних відповідей",
        "target_value": 10,
        "xp_reward": 60,
    },
    {
        "quest_type": "no_death_quiz",
        "description": "Пройди квіз без жодної помилки",
        "target_value": 1,
        "xp_reward": 75,
    },
]

import random

def get_or_create_daily_quests(user: User, db: Session) -> list[DailyQuest]:
    today = date.today()
    quests = db.query(DailyQuest).filter(
        DailyQuest.user_id == user.id,
        DailyQuest.quest_date == today,
    ).all()

    if quests:
        return quests

    # Генеруємо 3 квести на день (seed за датою щоб усі бачили одне)
    seed = int(today.strftime("%Y%m%d"))
    rng = random.Random(seed + hash(user.id) % 1000)
    selected = rng.sample(QUEST_DEFINITIONS, min(3, len(QUEST_DEFINITIONS)))

    new_quests = []
    for qdef in selected:
        q = DailyQuest(
            user_id=user.id,
            quest_date=today,
            quest_type=qdef["quest_type"],
            description=qdef["description"],
            target_value=qdef["target_value"],
            xp_reward=qdef["xp_reward"],
            current_value=0,
            is_completed=False,
        )
        db.add(q)
        new_quests.append(q)

    db.commit()
    for q in new_quests:
        db.refresh(q)
    return new_quests


def update_quest_progress(user: User, event_type: str, db: Session, increment: int = 1) -> list[dict]:
    """
    Оновлює прогрес квестів за подією.
    event_type: 'answer_correct' | 'complete_quiz' | 'defeat_boss' | 'no_death_quiz'
    Повертає список щойно завершених квестів.
    """
    today = date.today()
    quests = db.query(DailyQuest).filter(
        DailyQuest.user_id == user.id,
        DailyQuest.quest_date == today,
        DailyQuest.is_completed == False,
    ).all()

    completed_now = []
    for quest in quests:
        if quest.quest_type != event_type:
            continue
        quest.current_value = min(quest.current_value + increment, quest.target_value)
        if quest.current_value >= quest.target_value:
            quest.is_completed = True
            quest.completed_at = datetime.now(timezone.utc)
            add_xp(user, quest.xp_reward, db)
            completed_now.append({
                "quest_type": quest.quest_type,
                "description": quest.description,
                "xp_reward": quest.xp_reward,
            })
        db.add(quest)

    if completed_now:
        db.add(user)
    db.commit()
    return completed_now


def format_quest(q: DailyQuest) -> dict:
    return {
        "id": q.id,
        "quest_type": q.quest_type,
        "description": q.description,
        "target_value": q.target_value,
        "current_value": q.current_value,
        "xp_reward": q.xp_reward,
        "is_completed": q.is_completed,
        "progress_pct": round(q.current_value / q.target_value * 100),
    }
