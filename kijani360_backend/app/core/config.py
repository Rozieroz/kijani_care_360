import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "KijaniCare360"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Tree Conservation Platform for Kenya"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/kijanicare360"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # AI/LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]  # In production, specify actual hosts
    
    # File uploads
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "static/uploads")
    
    # Notifications
    ENABLE_PUSH_NOTIFICATIONS: bool = True
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    
    # Gamification
    ENABLE_ACHIEVEMENTS: bool = True
    ENABLE_LEADERBOARDS: bool = True
    
    # Development Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()