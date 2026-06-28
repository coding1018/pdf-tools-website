import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_tools.settings')

app = Celery('pdf_tools')

# Load configuration from Django settings, all configuration keys should have a `CELERY_` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule (for periodic tasks)
app.conf.beat_schedule = {
    'cleanup-old-files': {
        'task': 'tools.tasks.cleanup_old_files',
        'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
    'cleanup-expired-tasks': {
        'task': 'tools.tasks.cleanup_expired_tasks',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
