import os
from typing import Dict, List
from .default import DefaultSettings

class TestSettings(DefaultSettings):
    """Test configuration"""
    
    # Test overrides
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "test")
    DOCS_ENABLED: bool = os.getenv("DOCS_ENABLED", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    
    # CORS (more restrictive)
    CORS_ORIGINS: List[str] = [os.getenv("FRONTEND_URL", "https://yourdomain.test.com")]