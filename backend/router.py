from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import UserCreate, UserRead
from backend.database import new_session
from backend.models import User
from sqlalchemy.future import select

api_router = APIRouter(
    prefix='/users'
)

# Зависимость для получения сессии базы данных
async def get_db() -> AsyncSession:
    async with new_session() as session:
        yield session

# Добавление нового пользователя
@api_router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка, существует ли пользователь с таким email
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Создание нового пользователя
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        bio=user.bio,
        city=user.city
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

# Получение всех пользователей
@api_router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars()
    return users

# Получение пользователя по ID
@api_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
