from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "pyquest-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24        # 24 год
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = "postgresql://pyquest:devpassword@localhost:5432/pyquest"
    REDIS_URL: str = "redis://localhost:6379"

    JUDGE0_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
