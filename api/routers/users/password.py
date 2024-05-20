

@users.post("/password-reset-request", status_code=202)
@limiter.limit("1/second")
async def request_password_reset(
    request: Request,
    email: str,
    user_repository: UserRepository = Depends(get_user_repository),
    token_manager: TokenManager = Depends(get_token_manager)
):
    user = await user_repository.get_user_by_email(email)
    if user:
        token_type="password_reset"
        password_reset_token_lifetime = settings.PASSWORD_RESET_TOKEN_LIFESPAN_MINUTES
        reset_token = await token_manager.create_token(user.id, token_type, expires_delta=password_reset_token_lifetime)
        # Schedule sending the email in the background
        # fdsbackground_tasks.add_task(send_password_reset_email, user.email, reset_token)
        logger.info(f"Password reset requested for user {user.id}. Email queued.{reset_token}")

    # Return a generic message regardless of the email's existence in the DB
    return {"message": "If your email is registered with us, you will receive a password reset link shortly."}


@users.post("/password-reset")
async def reset_password(
    token: str,
    new_password: str,
    user_repository: UserRepository = Depends(get_user_repository),
    token_manager: TokenManager = Depends(get_token_manager)
):

    try:
        payload = await token_manager.validate_token(token)
        if "reset_password" not in payload.get("scope", []):
            raise HTTPException(status_code=403, detail="Invalid token")

        user_id = payload['sub']
        await user_repository.update_user_password(int(user_id), new_password)
        await token_manager.invalidate_user_tokens(int(user_id))

        return {"message": "Password successfully reset"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))