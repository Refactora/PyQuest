"""Quiz сервіс — логіка бою з крипами."""
import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.location import Location, Question
from app.models.progress import UserLocationProgress, QuizSession
from app.services.xp_service import add_xp, unlock_achievement, check_and_award_achievements
from app.services.daily_quest_service import update_quest_progress

QUESTIONS_PER_QUIZ = 10
XP_PER_CORRECT = 10
XP_QUIZ_COMPLETE = 50
XP_NO_DEATH_BONUS = 25
XP_PERFECT_SCORE_BONUS = 30


def _get_or_create_progress(user_id: str, location_id: int, db: Session) -> UserLocationProgress:
    p = db.query(UserLocationProgress).filter(
        UserLocationProgress.user_id == user_id,
        UserLocationProgress.location_id == location_id,
    ).first()
    if not p:
        p = UserLocationProgress(user_id=user_id, location_id=location_id, status="available")
        db.add(p)
        db.commit()
        db.refresh(p)
    return p


def start_quiz(user: User, location_slug: str, db: Session) -> dict:
    location = db.query(Location).filter(Location.slug == location_slug, Location.is_active == True).first()
    if not location:
        raise ValueError("Локацію не знайдено")

    progress = _get_or_create_progress(user.id, location.id, db)
    if progress.status == "locked":
        raise ValueError("Ця локація ще заблокована")

    db.query(QuizSession).filter(
        QuizSession.user_id == user.id, QuizSession.is_active == True
    ).update({"is_active": False, "completed_at": datetime.now(timezone.utc)})

    questions = db.query(Question).filter(
        Question.location_id == location.id, Question.is_active == True
    ).all()
    if len(questions) < QUESTIONS_PER_QUIZ:
        raise ValueError(f"Недостатньо питань (є {len(questions)}, потрібно {QUESTIONS_PER_QUIZ})")

    selected = random.sample(questions, QUESTIONS_PER_QUIZ)
    question_ids = [q.id for q in selected]

    session = QuizSession(
        user_id=user.id, location_id=location.id,
        questions_order=question_ids, current_index=0,
        hero_hp=user.hp_max, is_active=True,
    )
    db.add(session)
    if progress.status == "available":
        progress.status = "in_progress"
    db.commit()
    db.refresh(session)

    first_q = db.query(Question).filter(Question.id == question_ids[0]).first()
    return {
        "session_id": session.id,
        "location": {"id": location.id, "slug": location.slug, "name": location.name},
        "hero_hp": session.hero_hp,
        "question_number": 1,
        "total_questions": QUESTIONS_PER_QUIZ,
        "question": _fmt(first_q),
    }


def answer_question(user: User, session_id: str, question_id: int, selected_option: str, db: Session) -> dict:
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id, QuizSession.user_id == user.id, QuizSession.is_active == True,
    ).first()
    if not session:
        raise ValueError("Сесію не знайдено або вона вже завершена")

    q_ids = session.questions_order
    if session.current_index >= len(q_ids):
        raise ValueError("Питань більше немає")
    if q_ids[session.current_index] != question_id:
        raise ValueError("Невірний ID питання")

    question = db.query(Question).filter(Question.id == question_id).first()
    is_correct = selected_option.lower() == question.correct_option.lower()
    new_achievements = []
    completed_quests = []
    xp_gained = 0

    if is_correct:
        session.correct_answers += 1
        add_xp(user, XP_PER_CORRECT, db)
        xp_gained = XP_PER_CORRECT
        completed_quests += update_quest_progress(user, "answer_correct", db)
        if session.correct_answers == 1 and session.current_index == 0:
            if unlock_achievement(user, "first_blood", db):
                new_achievements.append("first_blood")
    else:
        session.wrong_answers += 1
        session.hero_hp -= 1

    if session.hero_hp <= 0:
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)
        progress = _get_or_create_progress(user.id, session.location_id, db)
        progress.quiz_attempts += 1
        db.add(progress)
        db.add(session)
        db.commit()
        return {
            "is_correct": is_correct, "correct_option": question.correct_option,
            "explanation": question.explanation, "xp_gained": 0,
            "hero_hp": 0, "hero_died": True, "is_quiz_done": False,
            "restart_message": "Герой загинув! Починаємо заново...",
        }

    session.current_index += 1
    is_last = session.current_index >= QUESTIONS_PER_QUIZ

    result = {
        "is_correct": is_correct, "correct_option": question.correct_option,
        "explanation": question.explanation, "xp_gained": xp_gained,
        "hero_hp": session.hero_hp, "hero_died": False,
        "questions_left": QUESTIONS_PER_QUIZ - session.current_index,
        "is_quiz_done": is_last,
        "new_achievements": new_achievements,
        "completed_quests": completed_quests,
    }

    if is_last:
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)
        no_death = session.hero_hp == user.hp_max
        perfect = session.correct_answers == QUESTIONS_PER_QUIZ
        bonus_xp = XP_QUIZ_COMPLETE
        add_xp(user, XP_QUIZ_COMPLETE, db)

        if no_death:
            add_xp(user, XP_NO_DEATH_BONUS, db)
            bonus_xp += XP_NO_DEATH_BONUS
            if unlock_achievement(user, "no_death_1", db):
                new_achievements.append("no_death_1")
            completed_quests += update_quest_progress(user, "no_death_quiz", db)
        if perfect:
            add_xp(user, XP_PERFECT_SCORE_BONUS, db)
            bonus_xp += XP_PERFECT_SCORE_BONUS
            if unlock_achievement(user, "perfectionist", db):
                new_achievements.append("perfectionist")

        progress = _get_or_create_progress(user.id, session.location_id, db)
        progress.quiz_completed = True
        progress.quiz_attempts += 1
        if session.correct_answers > progress.best_quiz_score:
            progress.best_quiz_score = session.correct_answers
        progress.no_death_run = no_death
        db.add(progress)

        completed_quests += update_quest_progress(user, "complete_quiz", db)
        new_achievements += check_and_award_achievements(user, db)

        result.update({
            "final_score": session.correct_answers, "total_questions": QUESTIONS_PER_QUIZ,
            "bonus_xp": bonus_xp, "next_step": "boss_fight",
            "no_death_run": no_death, "perfect_score": perfect,
            "new_achievements": new_achievements, "completed_quests": completed_quests,
        })
    else:
        next_q = db.query(Question).filter(Question.id == q_ids[session.current_index]).first()
        result["next_question"] = _fmt(next_q)
        result["question_number"] = session.current_index + 1

    db.add(session)
    db.add(user)
    db.commit()
    return result


def get_current_question(user: User, session_id: str, db: Session) -> dict:
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id, QuizSession.user_id == user.id, QuizSession.is_active == True,
    ).first()
    if not session:
        raise ValueError("Активну сесію не знайдено")
    q_id = session.questions_order[session.current_index]
    q = db.query(Question).filter(Question.id == q_id).first()
    return {
        "session_id": session.id, "hero_hp": session.hero_hp,
        "question_number": session.current_index + 1,
        "total_questions": QUESTIONS_PER_QUIZ,
        "correct_answers": session.correct_answers,
        "question": _fmt(q),
    }


def abandon_quiz(user: User, session_id: str, db: Session) -> dict:
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id, QuizSession.user_id == user.id, QuizSession.is_active == True,
    ).first()
    if not session:
        raise ValueError("Активну сесію не знайдено")
    session.is_active = False
    session.completed_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()
    return {"message": "Квіз перервано"}


def _fmt(q: Question) -> dict:
    return {
        "id": q.id, "question_text": q.question_text, "code_snippet": q.code_snippet,
        "option_a": q.option_a, "option_b": q.option_b,
        "option_c": q.option_c, "option_d": q.option_d,
        "difficulty": q.difficulty,
    }
