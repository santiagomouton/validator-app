import os
from typing import Dict, List
from .default import DefaultSettings

class ProductionSettings(DefaultSettings):
    """Production configuration"""
    
    # Production overrides
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DOCS_ENABLED: bool = os.getenv("DOCS_ENABLED", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "WARNING")
    
    # CORS (more restrictive)
    CORS_ORIGINS: List[str] = [os.getenv("FRONTEND_URL", "https://yourdomain.com")]
    