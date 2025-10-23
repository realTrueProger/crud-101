from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserORM


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[UserORM]:
        res = await self.session.execute(select(UserORM))
        return list(res.scalars().all())