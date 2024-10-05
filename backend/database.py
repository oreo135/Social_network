import asyncpg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка строки подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Функция для получения подключения к базе данных
async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

# Функция для создания таблиц в базе данных
async def create_tables():
    async with await get_connection() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                bio TEXT,
                city VARCHAR(100),
                birthdate DATE
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                birthdate DATE,
                city VARCHAR(100)
            )
        ''')

# Функция для удаления всех таблиц в базе данных
async def delete_tables():
    async with await get_connection() as conn:
        await conn.execute('''
            DROP TABLE IF EXISTS users
        ''')
        await conn.execute('''
            DROP TABLE IF EXISTS test_users
        ''')
