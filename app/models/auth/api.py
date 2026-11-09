from fastapi import APIRouter, Response, Request, HTTPException
from starlette import status

from app.core.database import db_dependency
from .schemas import UserSchema
from .services import register_user_service, login_user_services, refresh_token_services

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: db_dependency, user_data: UserSchema):
    user = register_user_service(db, user_data)

    return {
        "message": "The user has successfully registered!",
        "user_id": user
    }


@router.post("/login")
async def login(db: db_dependency, user_data: UserSchema, response: Response):
    access_token, refresh_token = login_user_services(db, user_data, response)
    return {
        "access_token": access_token,  # Already added to an HttpOnly cookie; remove in production
        "refresh_token": refresh_token  # Already added to an HttpOnly cookie; remove in production
    }


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    old_refresh_token = request.cookies.get("my_refresh_token")

    if not old_refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    new_access_token, new_refresh_token = refresh_token_services(old_refresh_token, response)

    return {
        "access_token": new_access_token, # Already added to an HttpOnly cookie; remove in production
        "refresh_access_token": new_refresh_token # Already added to an HttpOnly cookie; remove in production
    }
