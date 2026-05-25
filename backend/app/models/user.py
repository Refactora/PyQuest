import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_id = Column(Integer, nullable=False, default=1)

    level = Column(Integer, nullable=False, default=1)
    xp = Column(Integer, nullable=False, default=0)           # поточний XP у рівні
    xp_to_next = Column(Integer, nullable=False, default=100) # XP потрібно до наступного рівня
    total_xp = Column(Integer, nullable=False, default=0)     # всі XP за весь час (лідерборд)
    hp_max = Column(Integer, nullable=False, default=5)

    streak_days = Column(Integer, nullable=False, default=0)
    last_active = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    location_progress = relationship("UserLocationProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_sessions = relationship("QuizSession", back_populates="user", cascade="all, delete-orphan")
    boss_sessions = relationship("BossSession", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
