from fastapi import APIRouter
from config import get_settings
from .schemas.validator import ValidateMD5Request, ValidateMD5Response
from .services.validator import ValidatorService

router = APIRouter()


@router.get("/health", summary="Health check", tags=["health"])
def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }


@router.post(
    "/validate-md5",
    response_model=ValidateMD5Response,
    summary="Validate a JSON payload with MD5 hash",
    tags=["validation"])
def validate_md5(request: ValidateMD5Request):
    """
    Validate that the provided MD5 matches the payload.
    """
    validator_service = ValidatorService()
    return validator_service.validate_payload_with_md5(request.payload, request.md5)

