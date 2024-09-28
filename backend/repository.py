from backend.database import new_session
from backend.models import User
from backend.schemas import UserCreate, UserRead
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @classmethod
    async def add_one(cls, data: UserCreate) -> int:
        """
        Создание нового пользователя в базе данных
        """
        async with new_session() as session:  # Создаем новую сессию для работы с базой данных
            user_dict = data.model_dump()  # Преобразуем Pydantic объект в словарь

            user = User(**user_dict)  # Создаем объект пользователя на основе словаря
            session.add(user)  # Добавляем пользователя в сессию
            await session.flush()  # Применяем изменения (чтобы получить сгенерированный ID)
            await session.commit()  # Фиксируем изменения в базе данных
            return user.id  # Возвращаем ID созданного пользователя

    @classmethod
    async def find_all(cls) -> list[UserRead]:
        """
        Получение всех пользователей из базы данных
        """
        async with new_session() as session:  # Создаем новую сессию для работы с базой данных
            query = select(User)  # Создаем SQL-запрос для получения всех пользователей
            result = await session.execute(query)  # Выполняем запрос
            user_models = result.scalars().all()  # Получаем все объекты модели
            user_schemas = [UserRead.model_validate(user_model) for user_model in user_models]  # Преобразуем модели в схемы Pydantic
            return user_schemas  # Возвращаем список пользователей в виде схем
