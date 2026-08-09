import os
from functools import lru_cache
from .default import DefaultSettings
from .production import ProductionSettings
from .test import TestSettings

@lru_cache()
def get_settings():
    """Get settings based on ENVIRONMENT variable"""
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    if environment == 'production':
        return ProductionSettings()
    elif environment == 'test':
        return TestSettings()
    else:
        return DefaultSettings()
