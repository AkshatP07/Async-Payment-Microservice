from celery import Celery
import sys
import os
sys.path.append(os.path.dirname(__file__))
from app.core.config import settings


celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.autodiscover_tasks(["app.tasks"])
