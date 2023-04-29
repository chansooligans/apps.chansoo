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

from remindme import calendar, parsers, config
from remindme.main import MessageParser, RequestHandler

calendar_service = config.setup()

@csrf_exempt
def receive_sms(request):

    # Parse incoming message data
    message_body = request.POST.get('Body')
    sender_phone_number = request.POST.get('From')

    if str(sender_phone_number) != "+16502355273":
        return
    
    parser = MessageParser(message_body=message_body)
    parsed_event = parser.parse_message()
    print(parsed_event)

    if parser._type == "generic":
        return HttpResponse(str(parsed_event))
    
    handler = RequestHandler(
        parsed=parsed_event,
        calendar_service=calendar_service,
        ScheduledEvent=ScheduledEvent,
        sender_phone_number=sender_phone_number
    )

    return handler.process_request()
