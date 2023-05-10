from django.http import HttpResponse
from django.shortcuts import render
from django.forms.utils import ErrorList
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription, Today
import hashlib

def home(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_subscription = NewsletterSubscription.objects.filter(email=email).first()
            if existing_subscription:
                existing_subscription.delete()  # Delete the existing subscription
            form.save()  # Save the new subscription
            # Add a success message or redirect to a success page
        else:
            # debug print the errors to console
            print("Form errors:", form.errors)
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'tailorscoop/home.html', {'form': form})

def today_story(request):

    today_objects = Today.objects.order_by('-timestamp')
    first_today_object = today_objects.first()

    if first_today_object:
        content = first_today_object.content
    else:
        content = None  

    context = {'story_text': content}

    return render(request, 'tailorscoop/today.html', context)

def unsubscribe(request, hashed_email):
    try:
        subscription = NewsletterSubscription.objects.get(hashed_email=hashed_email)
        subscription.delete()
        message = "You have been unsubscribed from Tailored Scoop. We're sorry to see you go!"
    except NewsletterSubscription.DoesNotExist:
        message = "This email address is not subscribed to Tailored Scoop."

    context = {'message': message}
    return render(request, 'tailorscoop/unsubscribe.html', context)