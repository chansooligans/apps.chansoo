from celery import shared_task
from .models import ScheduledEvent
from datetime import datetime, timedelta
from src.remindme import sms
from time import sleep
from django.core.mail import send_mail

@shared_task(name="send_event_reminders")
def send_event_reminders():
    now = datetime.now()
    upcoming_events = ScheduledEvent.objects.filter(sent=False, start_time__lte=now + timedelta(minutes=15))

    for event in upcoming_events:
        sms.send_reminder(
            event.phone_number, 
            f"Reminder: {event.summary} starts at {event.start_time.strftime('%Y-%m-%d %I:%M %p')}"
        )
        event.sent = True
        event.save()
