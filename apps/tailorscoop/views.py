from django.shortcuts import render
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription, Today

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

    today_objects = Today.objects.order_by('-timestamp')
    first_today_object = today_objects.first()

    if first_today_object:
        content = first_today_object.content
    else:
        content = None  

    context = {'story_text': content}

    return render(request, 'tailorscoop/today.html', context)