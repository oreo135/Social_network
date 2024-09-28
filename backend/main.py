from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import create_tables
from backend.router import api_router  # Импортируем роутер для API

# Инициализация FastAPI приложения с жизненным циклом
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при запуске приложения
    await create_tables()
    print('Database ready')
    yield
    print('Shutting down')

app = FastAPI(lifespan=lifespan)

# Подключаем роутеры
app.include_router(api_router)

# Базовый эндпоинт для проверки статуса приложения
@app.get("/")
async def root():
    return {"message": "Welcome to the Social Network API"}
