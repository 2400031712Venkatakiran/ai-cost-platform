from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

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
    """FastAPI dependency: give each request its own session, then close it."""
    async with AsyncSessionLocal() as session:
        yield session