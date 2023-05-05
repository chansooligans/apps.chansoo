# models.py
from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    keywords = models.TextField()

    def __str__(self):
        return self.email