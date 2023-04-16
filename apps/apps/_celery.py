# project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings.dev')

app = Celery('apps', broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    #Scheduler Name
    'send_event_reminders-1min': {
        # Task Name (Name Specified in Decorator)
        'task': 'send_event_reminders',  
        # Schedule      
        'schedule': 30.0
    }
}