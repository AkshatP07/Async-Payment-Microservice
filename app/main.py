from fastapi import FastAPI
from app.api import payments, websocket
from app.db.session import Base, engine
import logging
logging.basicConfig(level=logging.INFO)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async Payment Microservice")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(payments.router, prefix="/payments")

