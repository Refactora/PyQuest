from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BossChallenge(Base):
    __tablename__ = "boss_challenges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("locations.id"), unique=True, nullable=False)

    title = Column(String(200), nullable=False)
    story_text = Column(Text, nullable=False)
    task_text = Column(Text, nullable=False)
    function_signature = Column(String(200), nullable=False)
    function_call_template = Column(String(300), nullable=False)  # наприклад: "find_max({input})"
    starter_code = Column(Text, nullable=False)
    test_cases = Column(JSON, nullable=False)   # [{input, expected_output, is_hidden, description}]
    hints = Column(JSON, nullable=False)         # [{order, text, hp_cost}]

    boss_hp = Column(Integer, nullable=False, default=100)
    time_limit_sec = Column(Integer, nullable=False, default=10)
    memory_limit_mb = Column(Integer, nullable=False, default=128)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    location = relationship("Location", back_populates="boss_challenge")
    boss_sessions = relationship("BossSession", back_populates="challenge", cascade="all, delete-orphan")
