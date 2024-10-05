import asyncpg
from backend.database import get_connection
from backend.schemas import UserCreate, UserRead, UserUpdate
from typing import List, Optional

class UserRepository:
    # Создание пользователя
    @staticmethod
    async def create_user(data: UserCreate) -> UserRead:
        conn = await get_connection()
        user_id = await conn.fetchval('''
            INSERT INTO users (first_name, last_name, email, password, bio, city, birthdate)
            VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id
        ''', data.first_name, data.last_name, data.email, data.password, data.bio, data.city, data.birthdate)
        await conn.close()
        return UserRead(
            id=user_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            bio=data.bio,
            city=data.city,
            birthdate=data.birthdate
        )

    # Получение всех пользователей
    @staticmethod
    async def get_all_users() -> List[UserRead]:
        conn = await get_connection()
        rows = await conn.fetch('''
            SELECT id, first_name, last_name, email, bio, city, birthdate FROM users
        ''')
        await conn.close()
        return [UserRead(**dict(row)) for row in rows]

    # Получение пользователя по ID
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[UserRead]:
        conn = await get_connection()
        row = await conn.fetchrow('''
            SELECT id, first_name, last_name, email, bio, city, birthdate FROM users WHERE id = $1
        ''', user_id)
        await conn.close()
        if row is None:
            return None
        return UserRead(**dict(row))

    # Обновление пользователя
    @staticmethod
    async def update_user(user_id: int, data: UserUpdate) -> Optional[UserRead]:
        conn = await get_connection()
        set_clauses = []
        values = []
        i = 1

        if data.first_name is not None:
            set_clauses.append(f"first_name = ${i}")
            values.append(data.first_name)
            i += 1

        if data.last_name is not None:
            set_clauses.append(f"last_name = ${i}")
            values.append(data.last_name)
            i += 1

        if data.bio is not None:
            set_clauses.append(f"bio = ${i}")
            values.append(data.bio)
            i += 1

        if data.city is not None:
            set_clauses.append(f"city = ${i}")
            values.append(data.city)
            i += 1

        if not set_clauses:
            await conn.close()
            return await UserRepository.get_user_by_id(user_id)

        values.append(user_id)
        set_clause_str = ', '.join(set_clauses)

        await conn.execute(f'''
            UPDATE users
            SET {set_clause_str}
            WHERE id = ${i}
        ''', *values)

        await conn.close()
        return await UserRepository.get_user_by_id(user_id)

    # Удаление пользователя
    @staticmethod
    async def delete_user(user_id: int) -> None:
        conn = await get_connection()
        await conn.execute('''
            DELETE FROM users WHERE id = $1
        ''', user_id)
        await conn.close()
