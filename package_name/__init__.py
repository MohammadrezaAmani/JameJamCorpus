from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import package_name.config as settings
from package_name.db.tables import create_tables

# engine = create_async_engine(
#     settings.DATABASE_URL, echo=settings.DEBUG, future=True
# )
# async_session = sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
# )

# SESSION = async_session()

from sqlalchemy.orm import scoped_session


def start() -> scoped_session:
    # Creating db engine and session
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)
    create_tables(engine)
    return scoped_session(
        sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    )


SESSION = start()
