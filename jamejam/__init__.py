import asyncio
import logging
from sqlalchemy import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from jamejam import config
from jamejam.db.tables import BASE
from sqlalchemy.engine import create_engine

if config.DEBUG:
    logging.basicConfig(level=logging.INFO)

if config.DATABASE_URL.lower().startswith("sqlite"):
    engine = create_async_engine(
        config.DATABASE_URL,
        echo=config.DATABASE_LOGGING,
        # pool_recycle=3600,
        future=True,
        poolclass=NullPool,
        connect_args={"timeout": 30},
    )
    sync_engine = create_engine(
        config.DATABASE_URL,
        echo=config.DATABASE_LOGGING,
        # pool_recycle=3600,
        future=True,
        poolclass=NullPool,
        connect_args={"timeout": 30},

    )

else:
    engine = create_async_engine(
        config.DATABASE_URL,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        echo=config.DATABASE_LOGGING,
        pool_recycle=3600,
        future=True,
    )
    sync_engine = create_engine(
        config.DATABASE_URL,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        echo=config.DATABASE_LOGGING,
        pool_recycle=3600,
    )


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)
        logging.info("Database tables created")


asyncio.run(init_db())


def get_session():
    yield AsyncSession(engine, expire_on_commit=False)


def get_sync_session():
    return sessionmaker(sync_engine)()
