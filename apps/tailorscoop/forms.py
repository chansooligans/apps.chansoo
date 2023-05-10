from django import forms
from .models import NewsletterSubscription
import hashlib

class NewsletterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField()
    keywords = forms.CharField(required=False)

    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'keywords']

    def clean_email(self):
        email = self.cleaned_data['email']
        existing_subscription = NewsletterSubscription.objects.filter(email=email).first()
        if existing_subscription:
            self.instance = existing_subscription  # Update the existing subscription

        # Add SHA256 encrypted copy of email
        hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
        self.instance.hashed_email = hashed_email

        return email

    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        if not keywords:
            return ''
        return keywords
