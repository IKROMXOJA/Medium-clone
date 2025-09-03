from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str

    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALG: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Email sozlamalari (FastAPI-Mail bilan mos)
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    FRONTEND_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
