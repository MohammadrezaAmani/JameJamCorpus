from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from package_name.db import create_tables
import package_name.config as settings


async def get_session():
    async_session = sessionmaker(
        create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True),
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session