from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# для работы нужно создать вручную postgres
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'fast_api_test'

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass