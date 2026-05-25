"""
Quiz сервіс — логіка бою з крипами.
"""
import random
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.location import Location, Question
from app.models.progress import UserLocationProgress, QuizSession
from app.services.xp_service import add_xp, check_and_award_achievements, unlock_achievement

QUESTIONS_PER_QUIZ = 10
XP_PER_CORRECT = 10
XP_QUIZ_COMPLETE = 50
XP_NO_DEATH_BONUS = 25
XP_PERFECT_SCORE_BONUS = 30


def get_or_create_progress(user_id: str, location_id: int, db: Session) -> UserLocationProgress:
    progress = db.query(UserLocationProgress).filter(
        UserLocationProgress.user_id == user_id,
        UserLocationProgress.location_id == location_id
    ).first()
    if not progress:
        progress = UserLocationProgress(user_id=user_id, location_id=location_id, status="available")
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress


def start_quiz(user: User, location_slug: str, db: Session) -> dict:
    location = db.query(Location).filter(Location.slug == location_slug, Location.is_active == True).first()
    if not location:
        raise ValueError("Локацію не знайдено")

    progress = get_or_create_progress(user.id, location.id, db)
    if progress.status == "locked":
        raise ValueError("Ця локація ще заблокована")

    # Закрити попередню активну сесію
    db.query(QuizSession).filter(
        QuizSession.user_id == user.id,
        QuizSession.is_active == True
    ).update({"is_active": False, "completed_at": datetime.now(timezone.utc)})

    # Отримати та перемішати питання
    questions = db.query(Question).filter(
        Question.location_id == location.id,
        Question.is_active == True
    ).all()

    if len(questions) < QUESTIONS_PER_QUIZ:
        raise ValueError(f"Недостатньо питань (є {len(questions)}, потрібно {QUESTIONS_PER_QUIZ})")

    selected = random.sample(questions, QUESTIONS_PER_QUIZ)
    question_ids = [q.id for q in selected]

    session = QuizSession(
        user_id=user.id,
        location_id=location.id,
        questions_order=question_ids,
        current_index=0,
        hero_hp=user.hp_max,
        is_active=True
    )
    db.add(session)

    # Оновити статус
    if progress.status == "available":
        progress.status = "in_progress"

    db.commit()
    db.refresh(session)

    first_question = db.query(Question).filter(Question.id == question_ids[0]).first()

    return {
        "session_id": session.id,
        "location": {"id": location.id, "slug": location.slug, "name": location.name},
        "hero_hp": session.hero_hp,
        "question_number": 1,
        "total_questions": QUESTIONS_PER_QUIZ,
        "question": _format_question(first_question),
    }


def answer_question(user: User, session_id: str, question_id: int, selected_option: str, db: Session) -> dict:
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id,
        QuizSession.user_id == user.id,
        QuizSession.is_active == True
    ).first()
    if not session:
        raise ValueError("Сесію не знайдено або вона вже завершена")

    question_ids = session.questions_order
    if session.current_index >= len(question_ids):
        raise ValueError("Питань більше немає")

    current_q_id = question_ids[session.current_index]
    if current_q_id != question_id:
        raise ValueError("Невірний ID питання")

    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise ValueError("Питання не знайдено")

    is_correct = (selected_option.lower() == question.correct_option.lower())
    xp_gained = 0
    new_achievements = []

    if is_correct:
        session.correct_answers += 1
        xp_result = add_xp(user, XP_PER_CORRECT, db)
        xp_gained = XP_PER_CORRECT

        # Перший правильний відповідь → ачівмент
        if session.correct_answers == 1 and session.current_index == 0:
            if unlock_achievement(user, "first_blood", db):
                new_achievements.append("first_blood")
    else:
        session.wrong_answers += 1
        session.hero_hp -= 1

    # Перевіряємо смерть
    if session.hero_hp <= 0:
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)

        # Збільшуємо лічильник спроб
        progress = get_or_create_progress(user.id, session.location_id, db)
        progress.quiz_attempts += 1
        db.add(progress)
        db.commit()

        return {
            "is_correct": is_correct,
            "correct_option": question.correct_option,
            "explanation": question.explanation,
            "xp_gained": 0,
            "hero_hp": 0,
            "hero_died": True,
            "is_quiz_done": False,
            "restart_message": "Герой загинув! Починаємо заново...",
        }

    session.current_index += 1
    is_last = session.current_index >= QUESTIONS_PER_QUIZ

    result = {
        "is_correct": is_correct,
        "correct_option": question.correct_option,
        "explanation": question.explanation,
        "xp_gained": xp_gained,
        "hero_hp": session.hero_hp,
        "hero_died": False,
        "questions_left": QUESTIONS_PER_QUIZ - session.current_index,
        "is_quiz_done": is_last,
        "new_achievements": new_achievements,
    }

    if is_correct:
        result["creep_killed"] = True

    if is_last:
        # Квіз завершено!
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)

        bonus_xp = 0
        no_death = session.hero_hp == user.hp_max  # жодного пропущеного удару
        perfect = session.correct_answers == QUESTIONS_PER_QUIZ

        completion_xp = XP_QUIZ_COMPLETE
        xp_result = add_xp(user, completion_xp, db)
        bonus_xp += completion_xp

        if no_death:
            ndb_result = add_xp(user, XP_NO_DEATH_BONUS, db)
            bonus_xp += XP_NO_DEATH_BONUS
            if unlock_achievement(user, "no_death_1", db):
                new_achievements.append("no_death_1")

        if perfect:
            perf_result = add_xp(user, XP_PERFECT_SCORE_BONUS, db)
            bonus_xp += XP_PERFECT_SCORE_BONUS
            if unlock_achievement(user, "perfectionist", db):
                new_achievements.append("perfectionist")

        # Оновлюємо прогрес
        progress = get_or_create_progress(user.id, session.location_id, db)
        progress.quiz_completed = True
        progress.quiz_attempts += 1
        if session.correct_answers > progress.best_quiz_score:
            progress.best_quiz_score = session.correct_answers
        progress.no_death_run = no_death
        db.add(progress)

        new_achievements += check_and_award_achievements(user, db)

        result.update({
            "final_score": session.correct_answers,
            "total_questions": QUESTIONS_PER_QUIZ,
            "bonus_xp": bonus_xp,
            "next_step": "boss_fight",
            "no_death_run": no_death,
            "perfect_score": perfect,
            "new_achievements": new_achievements,
        })
    else:
        # Наступне питання
        next_q_id = question_ids[session.current_index]
        next_q = db.query(Question).filter(Question.id == next_q_id).first()
        result["next_question"] = _format_question(next_q)
        result["question_number"] = session.current_index + 1

    db.add(session)
    db.add(user)
    db.commit()

    return result


def get_current_question(user: User, session_id: str, db: Session) -> dict:
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id,
        QuizSession.user_id == user.id,
        QuizSession.is_active == True
    ).first()
    if not session:
        raise ValueError("Активну сесію не знайдено")

    q_id = session.questions_order[session.current_index]
    question = db.query(Question).filter(Question.id == q_id).first()

    return {
        "session_id": session.id,
        "hero_hp": session.hero_hp,
        "question_number": session.current_index + 1,
        "total_questions": QUESTIONS_PER_QUIZ,
        "correct_answers": session.correct_answers,
        "question": _format_question(question),
    }


def _format_question(q: Question) -> dict:
    return {
        "id": q.id,
        "question_text": q.question_text,
        "code_snippet": q.code_snippet,
        "option_a": q.option_a,
        "option_b": q.option_b,
        "option_c": q.option_c,
        "option_d": q.option_d,
        "difficulty": q.difficulty,
    }
