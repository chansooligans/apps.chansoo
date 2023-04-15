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
            {"role": "system", "content": f"Today's date is {datetime.now()} unless otherwise specified."},
            {"role": "system", "content": f"""
                Classify the request as one of the following:
                - schedule
                - reminder
            """},
            {"role": "system", "content": """
                Do not include any explanations, only provide a  RFC8259 compliant JSON response following this format without deviation
                and make sure all keys are included in the object:
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
                    "classification": ["schedule" or "reminder"]
                }
                ```
                The JSON response:
            """}
        ]
    )
    
    response =  json.loads(response["choices"][0]["message"]["content"])

    for k in ["summary", "location", "description", "start", "end", "classification"]:
        if k not in response.keys():
            response[k] = ""

    return response