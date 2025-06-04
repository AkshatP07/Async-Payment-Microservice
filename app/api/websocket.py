from fastapi import APIRouter, WebSocket
from app.core.redis import redis_client

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/payments")
async def payment_ws(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe("payment_channel")

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"].decode("utf-8"))
    except Exception:
        await websocket.close()
        pubsub.close()
