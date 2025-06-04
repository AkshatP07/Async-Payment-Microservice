from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neonpost_owner:npg_F2LdPeYTt9JA@ep-orange-smoke-a1rx8t1x-pooler.ap-southeast-1.aws.neon.tech/neonpost?sslmode=require"

engine = create_engine(DATABASE_URL)
