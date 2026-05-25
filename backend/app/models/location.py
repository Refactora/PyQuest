from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    topic = Column(String(100), nullable=False)
    order_index = Column(Integer, unique=True, nullable=False)

    boss_name = Column(String(100), nullable=False)
    boss_sprite_id = Column(String(50), nullable=False)
    background_id = Column(String(50), nullable=False)
    enemy_sprite_id = Column(String(50), nullable=False)
    color_theme = Column(String(7), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    questions = relationship("Question", back_populates="location", cascade="all, delete-orphan")
    boss_challenge = relationship("BossChallenge", back_populates="location", uselist=False)
    user_progress = relationship("UserLocationProgress", back_populates="location")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)

    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'a', 'b', 'c', 'd'
    explanation = Column(Text, nullable=False)

    difficulty = Column(Integer, default=1)  # 1-3
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    location = relationship("Location", back_populates="questions")
