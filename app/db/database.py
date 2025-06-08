from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg:// your -url in async pg mode"
engine = create_async_engine(
    DATABASE_URL, 
    echo=True
)
