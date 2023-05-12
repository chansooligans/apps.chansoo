from django.contrib import admin
from .models import NewsletterSubscription, Today, ClickLog

admin.site.register(NewsletterSubscription)
admin.site.register(Today)
admin.site.register(ClickLog)