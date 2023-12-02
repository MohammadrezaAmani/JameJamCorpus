import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from package_name import config
from package_name.db.tables import BASE


if config.DATABASE_URL.lower().startswith("sqlite"):
    engine = create_async_engine(
        config.DATABASE_URL,
        pool_pre_ping=True,
        echo=config.DEBUG,
        pool_recycle=3600,
        future=True,
    )
else:
    engine = create_async_engine(
        config.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        echo_pool=config.DEBUG,
        echo=config.DEBUG,
        pool_recycle=3600,
        future=True,
    )


def session_factory():
    return scoped_session(
        sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    )


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)


asyncio.run(init_db())


def get_session():
    yield session_factory()
