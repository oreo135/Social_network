import asyncpg
import csv
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка строки подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")


# Функция для загрузки данных из CSV-файла в таблицу test_users
async def load_data_from_csv(csv_file_path: str):
    conn = await asyncpg.connect(DATABASE_URL)
    async with conn.transaction():
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # Извлечение данных из строки CSV
                first_name, last_name = row[0].split(' ')
                birthdate_str, city = row[1], row[2]

                # Преобразование строки с датой в объект datetime.date
                birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()

                # Выполнение SQL-запроса для вставки данных
                await conn.execute('''
                    INSERT INTO test_users (first_name, last_name, birthdate, city)
                    VALUES ($1, $2, $3, $4)
                ''', first_name, last_name, birthdate, city)
    await conn.close()


if __name__ == "__main__":
    import asyncio

    # "users_data.csv" путь к CSV-файлу
    asyncio.run(load_data_from_csv("users_data.csv"))
