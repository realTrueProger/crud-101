from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """Вход для создания"""
    pass

class UserUpdate(BaseModel):
    """Вход для обновления"""
    name: str | None
    email: str | None

class User(UserBase):
    """Выходная модель"""
    id: int

users: list[User] = [
    User(name="Vova", email="123@ya.ru", id=0),
    User(name="Sergey", email="555@ya.ru", id=1),
]

last_id = 1

@app.get("/", summary="Ping")
async def ping():
    return {"message": "ping ok"}

@app.get("/users", response_model=list[User], summary="List users")
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User, summary="Get user by id")
def get_user(user_id: int):
    for u in users:
        if u.id == user_id:
            return u
    raise HTTPException(404, detail="User not found")

@app.post("/users", response_model=User, summary="Create user")
def add_user(data: UserCreate):
    global last_id
    last_id += 1
    new_user = User(id=last_id, **data.model_dump())
    users.append(new_user)
    return new_user

@app.patch("/users/{user_id}", response_model=User, summary="Update user")
def update_user(user_id: int, data: UserUpdate):
    for idx, u in enumerate(users):
        if u.id == user_id:
            updated = u.model_copy(update=data.model_dump(exclude_unset=True))
            users[idx] = updated
            return updated
    raise HTTPException(404, detail="User not found")

@app.delete("/users/{user_id}", summary="Delete user")
def delete_user(user_id: int):
    for idx, u in enumerate(users):
        if u.id == user_id:
            users.pop(idx)
            return
    raise HTTPException(404, detail="User not found")