# Create your models here.
from django.db import models

class ScheduledEvent(models.Model):
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    phone_number = models.CharField(max_length=20)
    sent = models.BooleanField(default=False)
