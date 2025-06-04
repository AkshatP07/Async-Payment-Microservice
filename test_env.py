from app.core.celery_app import celery
print("Broker:", celery.conf.broker_url)
