from fastapi import FastAPI
from app.api import payments, websocket
from app.db.session import Base, engine
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Async Payment Microservice")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(payments.router, prefix="/payments")
