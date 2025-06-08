from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session                                # OLD: sync session import
from sqlalchemy.ext.asyncio import AsyncSession                      # NEW: async session import
from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentOut
from app.db.models import Payment
from app.tasks.payment_tasks import process_payment
from app.core.celery_app import celery  # <-- restored
import redis  # <-- restored
from app.core.config import settings  # <-- restored
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=PaymentOut)
# async def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):  # OLD sync session
async def create_payment(payload: PaymentCreate, db: AsyncSession = Depends(get_db)):  # NEW async session
    # Create payment record
    new_payment = Payment(amount=payload.amount, status="pending")
    db.add(new_payment)
    await db.commit()                    # NEW: await commit
    await db.refresh(new_payment)       # NEW: await refresh

    # Log celery info (once, not per request - move this to startup)
    logger.info(f"Celery broker: {celery.conf.broker_url}")
    logger.info(f"Celery backend: {celery.conf.result_backend}")

    # Trigger async processing (NO Redis ping - this was the bottleneck!)
    logger.info(f"[FastAPI] Triggering async payment for ID: {new_payment.id}")
    try:
        process_payment.delay(new_payment.id)
        logger.info(f"[FastAPI] Task queued successfully for ID: {new_payment.id}")
    except Exception as e:
        logger.error(f"Error calling celery task: {e}")
        raise e  # Keep original error handling

    return new_payment
