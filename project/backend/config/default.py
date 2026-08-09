import os
from typing import Dict, List
from pydantic_settings import BaseSettings

class DefaultSettings(BaseSettings):
    """Default configuration for development environment"""
    
    # App settings
    APP_NAME: str = "Validator API"
    APP_DESCRIPTION: str = "API thats validates hash values"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DOCS_ENABLED: bool = os.getenv("DOCS_ENABLED", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    CORS_ENABLED: bool = os.getenv("CORS_ENABLED", "True").lower() == "true"
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
