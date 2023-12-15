from celery import Celery


celery = Celery(__name__)
celery.autodiscover_tasks(['tasks'])
celery.conf.broker_url = "redis://redis:6379"
celery.conf.result_backend = "redis://redis:6379"
