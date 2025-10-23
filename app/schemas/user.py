from pydantic import BaseModel, EmailStr

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

class UserResponse(UserBase):
    """Выходная модель"""
    id: int
    model_config = {"from_attributes": True}