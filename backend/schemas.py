from typing import Optional
from pydantic import BaseModel, EmailStr

# Схема для создания нового пользователя
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    city: Optional[str] = None

# Схема для отображения информации о пользователе
class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True

# Схема для обновления данных пользователя
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    city: Optional[str] = None
