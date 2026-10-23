import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# The engine manages a pool of database connections.
# Creating it does NOT connect yet; connections are opened on first use.
engine = create_async_engine(
    settings.database_url.get_secret_value(),
    echo=False,
    pool_pre_ping=True,
)

# A factory that produces a new AsyncSession each time it is called.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: one session per request, always closed afterwards.

    This does not commit. Services call `await session.commit()` when a business
    operation succeeds. Anything uncommitted is discarded when the session closes.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def check_database_connection() -> bool:
    """Run `SELECT 1` to verify that PostgreSQL is reachable."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:  # noqa: BLE001 - any failure here simply means "not reachable"
        logger.exception("Database connectivity check failed")
        return False