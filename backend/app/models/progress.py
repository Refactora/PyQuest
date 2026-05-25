import uuid

from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text,
    ForeignKey, JSON, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserLocationProgress(Base):
    __tablename__ = "user_location_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # 'locked' | 'available' | 'in_progress' | 'completed'
    status = Column(String(20), nullable=False, default="locked")

    quiz_completed = Column(Boolean, default=False)
    boss_defeated = Column(Boolean, default=False)

    best_quiz_score = Column(Integer, default=0)
    quiz_attempts = Column(Integer, default=0)
    boss_attempts = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)

    first_try_boss = Column(Boolean, default=False)
    no_death_run = Column(Boolean, default=False)

    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="location_progress")
    location = relationship("Location", back_populates="user_progress")


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    questions_order = Column(JSON, nullable=False)  # список ID питань у перемішаному порядку
    current_index = Column(Integer, default=0)

    hero_hp = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)

    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="quiz_sessions")


class BossSession(Base):
    __tablename__ = "boss_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("boss_challenges.id"), nullable=False)

    hero_hp = Column(Integer, nullable=False)
    boss_hp = Column(Integer, nullable=False, default=100)
    hints_used = Column(Integer, default=0)
    submissions = Column(JSON, default=list)  # [{attempt, code, test_results, passed_count, timestamp}]

    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    is_won = Column(Boolean, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="boss_sessions")
    challenge = relationship("BossChallenge", back_populates="boss_sessions")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon_id = Column(String(50), nullable=False)
    xp_reward = Column(Integer, default=0)

    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
