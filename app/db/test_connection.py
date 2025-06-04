from app.db.session import engine

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("DB connection successful:", result.scalar())
except Exception as e:
    print("DB connection failed:", e)
