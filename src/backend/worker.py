from celery import Celery


celery = Celery(__name__)
celery.autodiscover_tasks(['tasks'])
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
celery.conf.event_serializer = 'pickle'
celery.conf.task_serializer = 'pickle'
celery.conf.result_serializer = 'pickle'
celery.conf.broker_url = "redis://redis:6379"
celery.conf.result_backend = "redis://redis:6379"
