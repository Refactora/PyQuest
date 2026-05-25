from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "pyquest-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 години

    DATABASE_URL: str = "sqlite:///./pyquest.db"

    # Judge0 (опціонально — для виконання коду у босс-файті)
    # Отримати на https://rapidapi.com/judge0-official/api/judge0-ce
    JUDGE0_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
