from logging import getLogger
from typing import List
from enum import Enum
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from core.security.schemas import APIKeyCreateResponseSchema, APIKeyCreateSchema, APIKeyReadSchema, APIKeyRevokeResponseSchema
from core.security.auth import get_current_active_user
from core.security.security_service import SecurityService
from core.dependencies import get_security_service
from core.security.models import UserContext


logger = getLogger(__name__)

router = APIRouter()


class RevokedStatus(str, Enum):
    active = "active"
    revoked = "revoked"
    all = "all"


@router.get("/", response_model=List[APIKeyReadSchema])
async def get_api_keys(
    revoked: RevokedStatus = Query(
        RevokedStatus.active,
        description="Filter API keys by revocation status: 'active', 'revoked', or 'all'. Defaults to 'active'."
    ),
    user_context: UserContext = Depends(get_current_active_user()),
    security_service: SecurityService = Depends(get_security_service),
):
    """
    Endpoint to get all API Key for the current user
    """
    
    current_user = user_context.user

    if revoked == RevokedStatus.active:
        revoked_filter = False
    elif revoked == RevokedStatus.revoked:
        revoked_filter = True
    else:  # RevokedStatus.all
        revoked_filter = None

    api_keys = await security_service.list_api_keys(
        user=current_user,
        revoked=revoked_filter
    )
    return api_keys


@router.post("/", response_model=APIKeyCreateResponseSchema)
async def create_api_key(
    api_key_request: APIKeyCreateSchema,
    security_service: SecurityService = Depends(get_security_service),
    current_user: UserContext = Depends(get_current_active_user())
):
    """
    Endpoint to create a new API Key for the authenticated user.
    """

    created_api_key, raw_api_key = await security_service.create_api_key(
        user=current_user.user,
        permissions=api_key_request.permissions,
        expires_in=api_key_request.expires_in,
    )

    return APIKeyCreateResponseSchema(
        api_key=raw_api_key,
        identifier=created_api_key.identifier,
        expires_at=created_api_key.expires_at
    )


@router.delete("/{id}", response_model=APIKeyRevokeResponseSchema)
async def revoked_api_key(
    id: UUID,
    user_context: UserContext = Depends(get_current_active_user()),
    security_service: SecurityService = Depends(get_security_service)
):
    """
    Endpoint to revoke (disable) an API Key for the authenticated user.
    """

    revoked_api_key = await security_service.revoke_api_key(api_key_id=id)

    if not revoked_api_key:
        raise HTTPException(status_code=404, detail="API Key not found")

    return APIKeyRevokeResponseSchema(
        id=revoked_api_key.id,
        identifier=revoked_api_key.identifier,
        revoked=revoked_api_key.revoked,
        revoked_at=revoked_api_key.revoked_at,
        message="API key has been successfully revoked."
    )
