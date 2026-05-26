"""XP та система рівнів PyQuest."""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.progress import UserLocationProgress, Achievement, UserAchievement


def xp_for_level(level: int) -> int:
    return int(100 * (level ** 1.5))


def hp_max_for_level(level: int) -> int:
    if level >= 20: return 10
    if level >= 15: return 8
    if level >= 10: return 7
    if level >= 5:  return 6
    return 5


def get_title_for_level(level: int) -> str:
    if level >= 25: return "🏆 Легенда PyQuest"
    if level >= 20: return "👑 Лорд Алгоритмів"
    if level >= 15: return "🔮 Архімаг Функцій"
    if level >= 10: return "⚔️ Лицар Синтаксису"
    if level >= 6:  return "🐛 Мисливець на Баги"
    if level >= 3:  return "✨ Юний Маг Коду"
    return "🌱 Новачок-Кодер"


def add_xp(user: User, amount: int, db: Session) -> dict:
    user.xp += amount
    user.total_xp += amount
    leveled_up = False
    levels_gained = []
    while user.xp >= user.xp_to_next:
        user.xp -= user.xp_to_next
        user.level += 1
        user.xp_to_next = xp_for_level(user.level + 1) - xp_for_level(user.level)
        user.hp_max = hp_max_for_level(user.level)
        leveled_up = True
        levels_gained.append(user.level)
    db.add(user)
    return {
        "xp_gained": amount, "leveled_up": leveled_up,
        "new_level": user.level, "levels_gained": levels_gained,
        "current_xp": user.xp, "xp_to_next": user.xp_to_next,
        "title": get_title_for_level(user.level),
    }


def unlock_achievement(user: User, slug: str, db: Session) -> bool:
    ach = db.query(Achievement).filter(Achievement.slug == slug).first()
    if not ach:
        return False
    already = db.query(UserAchievement).filter(
        UserAchievement.user_id == user.id, UserAchievement.achievement_id == ach.id
    ).first()
    if already:
        return False
    db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
    if ach.xp_reward > 0:
        add_xp(user, ach.xp_reward, db)
    return True


def check_and_award_achievements(user: User, db: Session) -> list[str]:
    new = []
    def award(slug):
        if unlock_achievement(user, slug, db): new.append(slug)

    if user.level >= 10: award("level_10")
    if user.level >= 20: award("level_20")

    all_prog = db.query(UserLocationProgress).filter(UserLocationProgress.user_id == user.id).all()
    completed = [p for p in all_prog if p.boss_defeated]
    if len(completed) >= 1:  award("boss_slayer")
    if len(completed) == 10: award("all_bosses"); award("completionist")
    return new


def update_streak(user: User, db: Session) -> dict:
    now = datetime.now(timezone.utc)
    bonus_xp = 0
    if user.last_active:
        last = user.last_active.replace(tzinfo=timezone.utc) if user.last_active.tzinfo is None else user.last_active
        delta = (now.date() - last.date()).days
        if delta == 1:
            user.streak_days += 1
            if user.streak_days == 3:
                bonus_xp = 30
                unlock_achievement(user, "streak_3", db)
            elif user.streak_days == 7:
                bonus_xp = 100
                unlock_achievement(user, "streak_7", db)
            elif user.streak_days == 30:
                bonus_xp = 500
                unlock_achievement(user, "streak_30", db)
        elif delta > 1:
            user.streak_days = 1
    else:
        user.streak_days = 1
    user.last_active = now
    db.add(user)
    result = {"streak_days": user.streak_days, "bonus_xp": bonus_xp}
    if bonus_xp > 0:
        result.update(add_xp(user, bonus_xp, db))
    return result
