from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.core.database import Base, engine

# Створюємо таблиці при старті (SQLite автоматично)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PyQuest API",
    description="🐍 Backend для PyQuest — RPG для вивчення Python",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "🟢 online",
        "message": "PyQuest API працює!",
        "docs": "/docs",
    }