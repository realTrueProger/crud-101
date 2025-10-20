from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def list_users(self) -> list[UserORM]:
        return await self.repo.list()