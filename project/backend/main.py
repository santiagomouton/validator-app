import urllib3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.logger import setup_logger
from config import get_settings
from api.v1.endpoints import router as api_v1_router

# Disable SSL warnings
urllib3.disable_warnings()

def create_app():
    """Create FastAPI application"""
    
    settings = get_settings()
    logger = setup_logger()
    
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.DOCS_ENABLED else None,
        redoc_url="/redoc" if settings.DOCS_ENABLED else None,
        openapi_url="/docs-json" if settings.DOCS_ENABLED else None,
    )

    # Add CORS if enabled
    if settings.CORS_ENABLED:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
           allow_headers=settings.CORS_ALLOW_HEADERS,
        )
        logger.info("CORS middleware enabled")

    # Add API routes
    app.include_router(api_v1_router, prefix="/api/v1")

    logger.info(f"🚀 {settings.APP_NAME} ready at http://{settings.HOST}:{settings.PORT}")
    return app

app = create_app()
