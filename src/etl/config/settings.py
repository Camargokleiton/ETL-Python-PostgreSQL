# src/etl/config/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str


    INPUT_PATH: str = "data/input"
    OUTPUT_PATH: str = "data/output"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
