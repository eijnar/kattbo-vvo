from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies.user_repository import get_user_repository
from core.security.auth import authenticate_user
from repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login")
async def login_post(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository)
):
    user = await authenticate_user(form_data.username, form_data.password, user_repository)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set user in session
    request.session["user"] = {"id": user.id, "username": user.email}

    try:
        client_id = request.query_params["client_id"]
        redirect_uri = request.query_params["redirect_uri"]
        scope = request.query_params["scope"]
        state = request.query_params.get("state", "")
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing query parameter: {e.args[0]}"
        )

    logger.info("REDIRECTING")
    # Redirect back to the authorize endpoint
    return RedirectResponse(
        url=f"/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}",
        status_code=303
    )
