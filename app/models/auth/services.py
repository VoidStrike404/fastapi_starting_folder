from authx import RequestToken
from fastapi import HTTPException
from pwdlib import PasswordHash
from starlette import status

from app.core.config import get_auth_security, get_auth_config
from app.core.security import set_auth_cookies
from app.models.users.models import User

pwd_context = PasswordHash.recommended()

def register_user_service(db, user_data):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with that username already exists")

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(username=user_data.username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user_services(db, user_data, response):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if not existing_user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )

    is_valid_password = pwd_context.verify(user_data.password, existing_user.hashed_password)

    if not is_valid_password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    security = get_auth_security()

    access_token = security.create_access_token(uid=str(existing_user.id))
    refresh_token = security.create_refresh_token(uid=str(existing_user.id))

    config = get_auth_config()

    set_auth_cookies(response, access_token, refresh_token, config)

    return {access_token, refresh_token}


def refresh_token_services(old_refresh_token, response):

    security = get_auth_security()

    try:
        request_token = RequestToken(
            token=old_refresh_token,
            location="cookies",
            type="refresh",
        )

        payload = security.verify_token(
            request_token,
            verify_csrf=False,
        )

        user_id = payload.sub

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token payload"
            )

        new_access_token = security.create_access_token(uid=str(user_id))
        new_refresh_token = security.create_refresh_token(uid=str(user_id))

        config = get_auth_config()
        set_auth_cookies(response, new_access_token, new_refresh_token, config)

        return new_access_token, new_refresh_token

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate refresh token: {str(e)}"
        )