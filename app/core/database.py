from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Create an asynchronous SQLAlchemy engine.
# This engine is responsible for connecting to the database specified in DATABASE_URL from settings.
# The `create_async_engine` function enables asynchronous database operations.
engine = create_async_engine(settings.DATABASE_URL)

# Create an asynchronous session maker.
# `async_sessionmaker` configures a factory for new AsyncSession objects.
# `autocommit=False` and `autoflush=False` ensure that transactions are managed explicitly.
# `bind=engine` links this session maker to our asynchronous database engine.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting an asynchronous database session.
# This `get_db` function is designed to be used with FastAPI's dependency injection system.
# It provides a database session to a request, and ensures it's properly closed afterwards.
async def get_db():
    # Asynchronously open a session.
    async with SessionLocal() as session:
        try:
            # Yield the session to the calling function (e.g., a FastAPI route).
            # This makes the session available for database operations within the request.
            yield session
        finally:
            # Ensure the session is closed after the request is finished,
            # releasing the database connection.
            await session.close()