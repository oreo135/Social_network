from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from database import delete_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("base clear")
    yield
    await create_tables()
    print('base ready')
    yield
    print('Off')

app = FastAPI(lifespan=lifespan)



