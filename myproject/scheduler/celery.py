from celery.schedules import crontab
from myproject.celery import app

app.conf.beat_schedule = {
    "update-task-status-every-minute": {
        "task": "scheduler.tasks.update_task_status",
        "schedule": crontab(minute="*"),
    },
} 