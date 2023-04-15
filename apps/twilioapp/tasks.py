from celery import shared_task
from .models import ScheduledEvent
from datetime import datetime, timedelta
from src.remindme import sms

@shared_task
def send_event_reminders():
    now = datetime.now()
    upcoming_events = ScheduledEvent.objects.filter(sent=False, start_time__lte=now + timedelta(minutes=15))

    for event in upcoming_events:
        sms.send_reminder(event.phone_number, f"Reminder: {event.summary} starts at {event.start_time.strftime('%Y-%m-%d %I:%M %p')}")
        event.sent = True
        event.save()
