from django.shortcuts import render
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription
from sqlalchemy import create_engine, text
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
    from src import config
    secrets = config.setup()
    user = secrets['mysql']['username']
    password = secrets['mysql']['password']
    host = secrets['mysql']['host']
    database = secrets['mysql']['database']
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}?charset=utf8mb4')
    with engine.begin() as conn:
        query = text("SELECT * FROM today ORDER BY timestamp desc")
        df = pd.read_sql_query(query, conn)
    summary = "blashdfklsdj;flksdjf;ksdfj dsfk;sdjfkdsjfs"
    context = {'story_text': summary}
    return render(request, 'tailorscoop/today.html', context)