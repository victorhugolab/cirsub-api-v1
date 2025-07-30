from pydantic_settings import BaseSettings
from typing import Literal, List
import os
from dotenv import load_dotenv

# --- Detectar entorno y cargar el archivo .env correspondiente ---
env_value = os.getenv("ENVIRONMENT", "local").lower()

if env_value == "local":
    env_file = ".env.local"
elif env_value in ["prod", "server"]:
    env_file = ".env.prod"
else:
    env_file = ".env.local"

load_dotenv(env_file)


# --- Configuración del entorno ---
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
        env_file = env_file
        env_file_encoding = "utf-8"
        extra = "ignore"


# Instancia global
settings = Settings()

# Log simple del entorno
print(f"⚙️ Entorno: {settings.ENVIRONMENT}")
