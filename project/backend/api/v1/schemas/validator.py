from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class ValidateMD5Request(BaseModel):
    """Request body for MD5 validation."""

    payload: Any = Field(..., description="JSON payload to hash")
    md5: str = Field(..., min_length=32, max_length=32, description="MD5 hash to validate")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payload": {"name": "Carlitos", "age": 66, "active": True},
                "md5": "dd0670cdfe8bb81517e561d22ad9c236",
            }
        }
    )


class ValidateMD5Response(BaseModel):
    """Response when the MD5 is valid."""

    md5: str = Field(..., description="The computed MD5")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "md5": "dd0670cdfe8bb81517e561d22ad9c236"
            }
        }
    )