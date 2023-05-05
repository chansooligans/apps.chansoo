# models.py
from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    keywords = models.TextField()

    def __str__(self):
        return self.email
    
# class Today(models.Model):
#     content = models.CharField(max_length=4096)
#     timestamp = models.DateTimeField()

#     class Meta:
#         db_table = 'today'
#         ordering = ['timestamp']
