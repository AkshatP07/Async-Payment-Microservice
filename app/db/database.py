from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://neonpost_owner:npg_F2LdPeYTt9JA@ep-orange-smoke-a1rx8t1x-pooler.ap-southeast-1.aws.neon.tech/neonpost"

engine = create_async_engine(
    DATABASE_URL, 
    echo=True
)