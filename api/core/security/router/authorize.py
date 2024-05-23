from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from core.security.services.auth_service import AuthorizationService
from core.dependencies.authorization_service import get_authorization_service
import logging 

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/authorize")
async def authorize(
    request: Request,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str = None,
    authorization_service: AuthorizationService = Depends(get_authorization_service)
):
    # Validate client
    logger.info(f"Validating")
    await authorization_service.validate_client(client_id, redirect_uri)

    # Check if the user is already authenticated
    user = request.session.get("user")
    logger.info(f"Findoing")
    if not user:
        logger.info("NO USER IS FOUND")
        # Redirect to login page if user is not authenticated
        login_url = authorization_service.get_login_url(client_id, redirect_uri, scope, state)
        return RedirectResponse(url=login_url, status_code=400)

    # Create authorization code
    auth_code = authorization_service.create_authorization_code(user["id"], client_id, scope)
    # Redirect to the client's redirect URI with the authorization code
    redirect_response = RedirectResponse(
        url=f"{redirect_uri}?code={auth_code}&state={state}",
        status_code=status.HTTP_302_FOUND
    )
    
    return redirect_response
