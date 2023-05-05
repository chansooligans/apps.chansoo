from django.shortcuts import render
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription, Today
import pandas as pd

def home(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        print(form)
        if form.is_valid():
            print("Form data:", form.cleaned_data) 
            print(form.cleaned_data)
            

            email = form.cleaned_data['email']
            existing_subscription = NewsletterSubscription.objects.filter(email=email).first()
            if existing_subscription:
                existing_subscription.delete()  # Delete the existing subscription
            form.save()  # Save the new subscription
            # Add a success message or redirect to a success page
        else:
            print("Form errors:", form.errors) 
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'tailorscoop/home.html', {'form': form})

def today_story(request):

    # today_objects = Today.objects.order_by('-timestamp')
    # today_df = pd.DataFrame.from_records(today_objects.values())

    context = {'story_text': "testing"}
    return render(request, 'tailorscoop/today.html', context)