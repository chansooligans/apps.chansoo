from django.contrib import admin
from .models import NewsletterSubscription, Today

admin.site.register(NewsletterSubscription)
admin.site.register(Today)