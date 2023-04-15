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
def schedule_event(calendar_service, event):
    created_event = (
        calendar_service.events()
        .insert(calendarId='chansoosong@gmail.com', body=event)
        .execute()
    )
    return created_event
