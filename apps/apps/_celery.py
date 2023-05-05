# project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings.prod')

app = Celery('apps', broker="redis://0.0.0.0:6379/0", backend="redis://0.0.0.0:6379/0")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    #Scheduler Name
    'send_event_reminders-5min': {
        # Task Name (Name Specified in Decorator)
        'task': 'send_event_reminders',  
        # Schedule      
        'schedule': 60.0
    }
}