from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentOut
from app.db.models import Payment
from app.tasks.payment_tasks import process_payment
from app.core.celery_app import celery  # <-- add this
import redis
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=PaymentOut)
async def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(amount=payload.amount, status="pending")
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    # Test Redis ping
    r = redis.Redis.from_url(settings.REDIS_URL)
    try:
        r.ping()
        logger.info("Redis ping OK")
    except Exception as e:
        logger.error(f"Redis ping failed: {e}")

    # Log celery broker/backend
    logger.info(f"Celery broker: {celery.conf.broker_url}")
    logger.info(f"Celery backend: {celery.conf.result_backend}")

    # Trigger async processing
    logger.info(f"[FastAPI] Triggering async payment for ID: {new_payment.id}")
    try:
        process_payment.delay(new_payment.id)
    except Exception as e:
        logger.error(f"Error calling celery task: {e}")
        raise e

    return new_payment
