import asyncpg
from backend.database import get_connection
from backend.schemas import UserCreate, UserRead

class UserRepository:
    @staticmethod
    async def create_user(data: UserCreate) -> UserRead:
        conn = await get_connection()
        user_id = await conn.fetchval('''
            INSERT INTO users (first_name, last_name, email, password, bio, city)
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
        ''', data.first_name, data.last_name, data.email, data.password, data.bio, data.city)
        await conn.close()
        return UserRead(
            id=user_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            bio=data.bio,
            city=data.city
        )

    @staticmethod
    async def get_all_users() -> list[UserRead]:
        conn = await get_connection()
        rows = await conn.fetch('''
            SELECT id, first_name, last_name, email, bio, city FROM users
        ''')
        await conn.close()
        return [UserRead(**dict(row)) for row in rows]

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserRead:
        conn = await get_connection()
        row = await conn.fetchrow('''
            SELECT id, first_name, last_name, email, bio, city FROM users WHERE id = $1
        ''', user_id)
        await conn.close()
        if row is None:
            return None
        return UserRead(**dict(row))
