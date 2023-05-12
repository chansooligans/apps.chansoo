# models.py
import uuid
from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    hashed_email = models.CharField(max_length=64, blank=True)
    keywords = models.TextField()

    def __str__(self):
        return self.email
    
class Today(models.Model):
    content = models.CharField(max_length=8096)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'today'
        ordering = ['timestamp']

class ClickLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    hashed_email = models.CharField(max_length=255)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hashed_email}: {self.url}"
