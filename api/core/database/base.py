import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError

from ..config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.SQL_DATABASE_URL

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.SQL_DEBUG_MODE
    )
    logger.info("Async engine created successfully.")
except SQLAlchemyError as e:
    logger.error(f"Error creating async engine: {e}")
    raise

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base: DeclarativeMeta = declarative_base()


async def get_db():
    logger.info("Creating a new database session.")
    try:
        async with AsyncSessionLocal() as session:
            yield session
            logger.info("Database session created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error during database session creation: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


async def create_tables():
    logger.info("Creating database tables.")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise