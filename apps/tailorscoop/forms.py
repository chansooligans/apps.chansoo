from django import forms
from .models import NewsletterSubscription

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
        return email

    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        if not keywords:
            return ''
        return keywords
