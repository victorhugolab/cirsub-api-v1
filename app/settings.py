# app/settings.py

from pydantic_settings import BaseSettings
from typing import Literal, List


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "SERVER", "desconocido", "prod"] = "desconocido"

    DB_DRIVER: str
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://tu-dominio.com"
    ]

    class Config:
        env_file = ".env.local"  # ✅ ¡Agregado!
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

print(f"⚙️ Entorno: {settings.ENVIRONMENT}")
