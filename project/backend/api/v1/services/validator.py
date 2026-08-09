import hashlib
import json
import string
from typing import Any, Dict
from config.logger import logger
from fastapi import HTTPException, status


class ValidatorService:
    """Service layer for MD5."""

    def validate_payload_with_md5(self, payload: Any, md5: str) -> Dict[str, Any]:
        """Validate a payload with the provided MD5 hash."""
        logger.info("Validating MD5 hash for incoming payload")

        if not isinstance(md5, str) or len(md5) != 32 or any(char not in string.hexdigits for char in md5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Provided MD5 must be a 32-character hexadecimal string"}
            )
        normalized_payload = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        )
        md5_hash = hashlib.md5(normalized_payload.encode("utf-8")).hexdigest()

        if md5_hash != md5.lower():
            raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"message": "MD5 does not match the provided payload"}
                        )
        return {
            "md5": md5_hash
        }

