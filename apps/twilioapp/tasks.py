from celery import shared_task
from .models import ScheduledEvent
from datetime import datetime, timedelta
from src.remindme import sms
from time import sleep
import pytz
from django.core.mail import send_mail

@shared_task(name="send_event_reminders")
def send_event_reminders():
    now = datetime.now(pytz.utc)
    upcoming_events = ScheduledEvent.objects.filter(sent=False, start_time__lte=now + timedelta(minutes=15), start_time__gte=now)
    print(upcoming_events)

    for event in upcoming_events:

        print(event.start_time)
        edt_time = (
            event.start_time
            .astimezone(pytz.timezone('US/Eastern'))
            .strftime('%Y-%m-%d %I:%M %p')
        )
        print(edt_time)

        sms.send_reminder(
            event.phone_number, 
            f"Reminder: {event.summary} starts at {edt_time}; {event.description}"
        )
        event.sent = True
        event.save()
