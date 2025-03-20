import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.worker_pool = 'solo'

# Beat schedule
app.conf.beat_schedule = {
    "update-task-status-every-minute": {
        "task": "scheduler.tasks.update_task_status",
        "schedule": crontab(minute="*"),
    },
} 