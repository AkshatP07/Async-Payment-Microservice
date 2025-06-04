from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Payment
from app.core.redis import redis_client
import time

@shared_task
def process_payment(payment_id: int):
    print(f"[Celery] Start processing payment ID: {payment_id}")
    
    time.sleep(20)

    db: Session = SessionLocal()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            print(f"[Celery] Found payment with ID {payment.id}, current status: {payment.status}")
            payment.status = "completed"
            db.commit()
            print(f"[Celery] Updated status to: {payment.status}")
        else:
            print(f"[Celery] Payment ID {payment_id} not found in DB.")
    except Exception as e:
        db.rollback()
        print(f"[Celery] Exception while updating payment: {e}")
    finally:
        db.close()

    redis_client.publish("payment_channel", f"{payment_id}:completed")
