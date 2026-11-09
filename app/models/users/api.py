from fastapi import APIRouter

from app.core.database import db_dependency
from .models import User

router = APIRouter(tags=["Users"])

@router.get("/get_all_users")
async def get_all_users(db: db_dependency):
    all_users = db.query(User).all()
    return all_users