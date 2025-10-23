from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_session
from app.schemas.user import UserResponse
from app.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@user_router.get("", response_model=list[UserResponse])
async def list_users(svc: UserService = Depends(get_user_service)):
    return await svc.list_users()
