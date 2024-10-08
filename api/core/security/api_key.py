from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import logging

logger = logging.getLogger(__name__)

API_KEY_NAME = "x-api-key"
API_KEY = "6a72e1bd-92a6-4ada-b34d-c00eb9c62bdf"  # Ideally, this should come from an environment variable

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    logger.info(f"Received API key: {api_key_header}")
    if api_key_header == API_KEY:
        return api_key_header
    else:
        logger.error("Invalid API key")
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
