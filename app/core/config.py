from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Teamify"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/fluffypotato"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # First admin seed (set these in .env)
    FIRST_ADMIN_EMAIL: str = "admin@example.com"
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "changeme123"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
