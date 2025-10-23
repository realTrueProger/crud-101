from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import Base, engine
from app.routers.user_router import user_router
from app.models.user import UserORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(bind=engine, expire_on_commit=False) as db:
        exists = await db.scalar(select(UserORM.id).limit(1))

        if exists is None:
            db.add_all([
                UserORM(name="Vladimir", email="sollo@example.com"),
                UserORM(name="Sergey", email="bac@example.com"),
            ])
            await db.commit()

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/", summary="Ping")
async def ping():
    return {"message": "ping ok"}

#
# @app.get("/users/{user_id}", response_model=User, summary="Get user by id")
# def get_user(user_id: int):
#     for u in users:
#         if u.id == user_id:
#             return u
#     raise HTTPException(404, detail="User not found")
#
# @app.post("/users", response_model=User, summary="Create user")
# def add_user(data: UserCreate):
#     global last_id
#     last_id += 1
#     new_user = User(id=last_id, **data.model_dump())
#     users.append(new_user)
#     return new_user
#
# @app.patch("/users/{user_id}", response_model=User, summary="Update user")
# def update_user(user_id: int, data: UserUpdate):
#     for idx, u in enumerate(users):
#         if u.id == user_id:
#             updated = u.model_copy(update=data.model_dump(exclude_unset=True))
#             users[idx] = updated
#             return updated
#     raise HTTPException(404, detail="User not found")
#
# @app.delete("/users/{user_id}", summary="Delete user")
# def delete_user(user_id: int):
#     for idx, u in enumerate(users):
#         if u.id == user_id:
#             users.pop(idx)
#             return
#     raise HTTPException(404, detail="User not found")
