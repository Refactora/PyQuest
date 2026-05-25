from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, locations, quiz, boss, profile, leaderboard
from app.core.database import Base, engine

# Імпортуємо всі моделі щоб SQLAlchemy їх зареєстрував
import app.models  # noqa: F401

# Створюємо таблиці при старті
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PyQuest API",
    description="🐍 Backend для PyQuest — RPG для вивчення Python",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(locations.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(boss.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "🟢 online",
        "message": "PyQuest API v2.0 працює!",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth/register | /api/auth/login | /api/auth/me",
            "locations": "/api/locations | /api/locations/{slug}",
            "quiz": "/api/quiz/start | /api/quiz/answer | /api/quiz/session/{id}",
            "boss": "/api/boss/start | /api/boss/submit | /api/boss/hint",
            "profile": "/api/profile | /api/profile/avatar",
            "leaderboard": "/api/leaderboard",
        },
    }
