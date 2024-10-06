from fastapi import APIRouter, HTTPException, Depends
from backend.schemas import UserCreate, UserRead
from backend.repository import UserRepository

api_router = APIRouter(
    prefix='/users'
)

# Добавление нового пользователя
@api_router.post("/", response_model=UserRead)
async def create_user(user: UserCreate):
    existing_user = await UserRepository.get_user_by_id(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = await UserRepository.create_user(user)
    return new_user

# Получение всех пользователей
@api_router.get("/", response_model=list[UserRead])
async def get_users():
    return await UserRepository.get_all_users()

@api_router.get("/search", response_model=list[UserRead])
async def search_users(first_name: str, last_name: str):
    return await UserRepository.search_users(first_name, last_name)


# Получение пользователя по ID
@api_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int):
    user = await UserRepository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

