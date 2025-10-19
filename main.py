from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Base, engine, get_session
from models import UserORM

@asynccontextmanager
async def lifespan(app: FastAPI):
    # выполняется при старте приложения
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        # проверим, есть ли уже юзеры
        users_exist = db.scalar(select(UserORM).limit(1))
        if not users_exist:
            db.add_all([
                UserORM(name="Vladimir", email="sollo@example.com"),
                UserORM(name="Sergey", email="bac@example.com"),
            ])
            db.commit()

    yield

    # выполняется при остановке приложения (если нужно что-то почистить)
    # например: engine.dispose()
    engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.get("/", summary="Ping")
async def ping():
    return {"message": "ping ok"}

@app.get("/users")
def list_users(db: Session = Depends(get_session)):
    return db.execute(select(UserORM)).scalars().all()
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