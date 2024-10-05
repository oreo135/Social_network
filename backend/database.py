import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

# Настрой строку подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Функция для получения подключения к базе данных
async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

# Функция для создания таблиц в базе данных
async def create_tables():
    conn = await get_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            bio TEXT,
            city VARCHAR(100)
        )
    ''')
    await conn.close()

# Функция для удаления всех таблиц в базе данных
async def delete_tables():
    conn = await get_connection()
    await conn.execute('''
        DROP TABLE IF EXISTS users
    ''')
    await conn.close()
