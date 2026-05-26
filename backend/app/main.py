from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api import auth, locations, quiz, boss, profile, leaderboard, daily_quests
from app.core.config import settings
import app.models  # noqa

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PyQuest API",
    description="🐍 Backend для PyQuest — Python RPG",
    version="2.1.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,         prefix="/api")
app.include_router(locations.router,    prefix="/api")
app.include_router(quiz.router,         prefix="/api")
app.include_router(boss.router,         prefix="/api")
app.include_router(profile.router,      prefix="/api")
app.include_router(leaderboard.router,  prefix="/api")
app.include_router(daily_quests.router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {"status": "🟢 online", "version": "2.1.0", "docs": "/docs"}
