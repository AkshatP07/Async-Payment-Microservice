import os
from dotenv import load_dotenv

# SQLAlchemy async engine and session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Base class for ORM models
from sqlalchemy.orm import declarative_base

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async engine with connection pooling and other configurations
engine = create_async_engine(
    DATABASE_URL,
    echo=True,              # Log SQL queries to stdout (useful for debugging)
    pool_size=20,           # Number of connections in the pool
    max_overflow=80,        # Additional connections beyond pool_size
    pool_timeout=30,        # Wait time in seconds before giving up on getting a connection
    pool_recycle=3600,      # Recycle connections after 1 hour
)

# Create the async session factory using async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,    # Use the async version of the Session
    expire_on_commit=False, # Keep attributes available after commit
)

# Base class for all models to inherit from
Base = declarative_base()

# Dependency to get the database session (used in FastAPI routes and elsewhere)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
