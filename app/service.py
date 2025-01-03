from celery import Celery
import os
import redis


redis_client = redis.Redis(host=os.environ["REDIS_HOST"], decode_responses=True)
celery_app = Celery(
    'tasks',
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_RESULT_BACKEND"],
    include=['app.tasks']
)
