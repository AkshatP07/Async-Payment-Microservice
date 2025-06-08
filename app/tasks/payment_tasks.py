# Import Celery's shared_task decorator to define a task that can be run asynchronously
from celery import shared_task

# Import asyncio to run async functions inside a normal (sync) Celery task
import asyncio

# SQLAlchemy async session class
from sqlalchemy.ext.asyncio import AsyncSession

# SQLAlchemy select function for building SQL queries
from sqlalchemy import select

# Async session factory defined in your db/session.py
from app.db.session import AsyncSessionLocal

# Payment model (ORM class)
from app.db.models import Payment

# Redis client for publishing payment updates (used to notify frontend or other services)
from app.core.redis import redis_client

# Define a Celery task function — this is a SYNC wrapper that runs the actual async logic
@shared_task
def process_payment(payment_id: int):
    print(f"[Celery] Start processing payment ID: {payment_id}")
    
    # Run the actual async processing logic inside an event loop
    asyncio.run(_process_payment_async(payment_id))


# Actual async logic to process a payment
async def _process_payment_async(payment_id: int):
    # Create a new async DB session using context manager
    async with AsyncSessionLocal() as db:
        try:
            # Fetch the payment entry by ID
            result = await db.execute(select(Payment).where(Payment.id == payment_id))
            payment = result.scalar_one_or_none()

            if payment:
                print(f"[Celery] Found payment with ID {payment.id}, current status: {payment.status}")
                
                # Mark the payment as completed
                payment.status = "completed"
                await db.commit()  # Commit the DB transaction

                print(f"[Celery] COMMITTED - Updated status to: {payment.status}")

                # Optional: re-fetch the record to confirm it was updated
                result = await db.execute(select(Payment).where(Payment.id == payment_id))
                updated_payment = result.scalar_one_or_none()
                print(f"[Celery] VERIFIED - Status after commit: {updated_payment.status}")

            else:
                # Log if payment record not found
                print(f"[Celery] Payment ID {payment_id} not found in DB.")

        except Exception as e:
            # Rollback if there was an error during transaction
            await db.rollback()
            print(f"[Celery] Exception while updating payment: {e}")
            raise e  # Reraise so Celery logs the failure

    # After DB update, notify via Redis pub/sub that payment is completed
    redis_client.publish("payment_channel", f"{payment_id}:completed")
