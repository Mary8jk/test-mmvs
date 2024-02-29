from celery import Celery


app = Celery('video_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

