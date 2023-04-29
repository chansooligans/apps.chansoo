from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilioapp.models import ScheduledEvent

import openai
from pathlib import Path
from twilio.rest import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
import yaml
from datetime import datetime
from django.core.mail import send_mail
import json

from remindme import calendar, gpt

try:
    with open('/home/chansoo/projects/apps.chansoo/apps/twilioapp/api.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except:
    with open('/home/bitnami/projects/apps.chansoo/apps/twilioapp/api.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

OPENAI_API_KEY = config['openai']['api_key']
TWILIO_ACCOUNT_SID = config['twilio']['account_sid']
TWILIO_AUTH_TOKEN = config['twilio']['auth_token']
TWILIO_PHONE_NUMBER = config['twilio']['phone_number']

openai.api_key = OPENAI_API_KEY
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
    GOOGLE_SERVICE_ACCOUNT_FILE = f'/home/chansoo/projects/apps.chansoo/apps/twilioapp/credentials.json'
    google_credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE)
    calendar_service = build('calendar', 'v3', credentials=google_credentials)
except:
    GOOGLE_SERVICE_ACCOUNT_FILE = f'/home/bitnami/projects/apps.chansoo/apps/twilioapp/credentials.json'
    google_credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE)
    calendar_service = build('calendar', 'v3', credentials=google_credentials)

@csrf_exempt
def receive_sms(request):

    # Parse incoming message data
    message_body = request.POST.get('Body')
    sender_phone_number = request.POST.get('From')

    if str(sender_phone_number) != "+16502355273":
        return

    if message_body.startswith("openai"):
        return gpt.openai_standard(message_body)

    parsed_event = gpt.get_gpt4_schedule_response(message_body)

    if parsed_event["classification"] == "schedule":
    
        calendar.schedule_event(calendar_service, parsed_event)

        # Start our TwiML response
        resp = MessagingResponse()
        
        dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
        start_time = dt.strftime('%Y-%m-%d at %-I:%M%p')

        # Determine the right reply for this message
        resp.message(f"""Your event '{parsed_event["summary"]}' on {start_time} is scheduled""")
        
        return HttpResponse(str(resp))

    elif parsed_event["classification"] == "reminder":
        print(parsed_event.keys())
        event = ScheduledEvent(
            summary=parsed_event["summary"],
            location=parsed_event["location"],
            description=parsed_event["description"],
            start_time=parsed_event["start"]["dateTime"],
            end_time=parsed_event["end"]["dateTime"],
            phone_number=sender_phone_number,
        )
        event.save()        
        print('saved')

        # Start our TwiML response
        resp = MessagingResponse()
        
        dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
        start_time = dt.strftime('%Y-%m-%d at %-I:%M%p')

        # Determine the right reply for this message
        resp.message(f"""Your reminder '{parsed_event["summary"]}' on {start_time} is scheduled""")

        return HttpResponse(str(resp))
