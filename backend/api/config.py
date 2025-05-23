from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Основные настройки
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Food Management System"
    
    # Настройки CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:80",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:5501",
        "http://127.0.0.1:80",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501"
    ]
    
    # Настройки безопасности
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 