from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv() # Загружаем переменные окружения из .env файла

# Настрой строку подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
# Создание движка для подключения к базе данных PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной сессии для работы с базой данных
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Функция для создания всех таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для удаления всех таблиц в базе данных
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
