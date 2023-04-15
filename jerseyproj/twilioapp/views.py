from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

import openai
import os
from twilio.rest import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
import yaml
from datetime import datetime
import json

with open('/home/bitnami/projects/jerseystuff/api.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

OPENAI_API_KEY = config['openai']['api_key']
TWILIO_ACCOUNT_SID = config['twilio']['account_sid']
TWILIO_AUTH_TOKEN = config['twilio']['auth_token']
TWILIO_PHONE_NUMBER = config['twilio']['phone_number']
GOOGLE_SERVICE_ACCOUNT_FILE = config['google']['service_account_file']

openai.api_key = OPENAI_API_KEY
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
google_credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE)
calendar_service = build('calendar', 'v3', credentials=google_credentials)

def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps with scheduling and reminders."},
            {"role": "user", "content": prompt},
            {"role": "system", "content": "Default timeZone is America/New_York unless otherwise specified."},
            {"role": "system", "content": f"Assume year is {datetime.now().year} unless otherwise specified."},
            {"role": "system", "content": """
                Do not include any explanations, only provide a  RFC8259 compliant JSON response following this format without deviation:
                ```
                {
                    "summary": "Google I/O 2015",
                    "location": "800 Howard St., San Francisco, CA 94103",
                    "description": "A chance to hear more about Google\'s developer products.",
                    "start": {
                        "dateTime": "2023-04-16T09:00:00-07:00",
                        "timeZone": "America/New_York",
                    },
                    "end": {
                        "dateTime": "2023-04-16T17:00:00-07:00",
                        "timeZone": "America/New_York",
                    },
                }
                ```
                The JSON response:
            """}
        ]
    )
    return response

# Function to schedule an event on Google Calendar
def schedule_event(event):
    created_event = (
        calendar_service.events()
        .insert(calendarId='chansoosong@gmail.com', body=event)
        .execute()
    )
    return created_event

# Function to send a reminder using Twilio
def send_reminder(phone_number, message):
    twilio_client.messages.create(
        body=message,
        from_='<your_twilio_phone_number>',
        to=phone_number,
    )

@csrf_exempt
def receive_sms(request):

    # Parse incoming message data
    message_body = request.POST.get('Body')
    sender_phone_number = request.POST.get('From')

    openai_response = get_gpt4_response(message_body)
    parsed_event = json.loads(openai_response["choices"][0]["message"]["content"])
    scheduled_event = schedule_event(parsed_event)

    # Start our TwiML response
    resp = MessagingResponse()
    
    dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
    start_time = dt.strftime('%Y-%m-%d at %-I%p')

    # Determine the right reply for this message
    resp.message(f"""Your event '{parsed_event["summary"]}' on {start_time} is scheduled""")
    
    return HttpResponse(str(resp))
