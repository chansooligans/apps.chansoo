from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms.utils import ErrorList
from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscription, Today, ClickLog
import base64


def home(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            existing_subscription = NewsletterSubscription.objects.filter(
                email=email
            ).first()
            if existing_subscription:
                existing_subscription.delete()  # Delete the existing subscription
            form.save()  # Save the new subscription
            # Add a success message or redirect to a success page
        else:
            # debug print the errors to console
            print("Form errors:", form.errors)
    else:
        form = NewsletterSubscriptionForm()

    return render(request, "tailorscoop/home.html", {"form": form})


def today_story(request):
    today_objects = Today.objects.order_by("-timestamp")
    first_today_object = today_objects.first()

    if first_today_object:
        content = first_today_object.content
    else:
        content = None

    context = {"story_text": content}

    return render(request, "tailorscoop/today.html", context)


def unsubscribe_confirm(request, hashed_email):
    try:
        subscription = NewsletterSubscription.objects.get(hashed_email=hashed_email)
        subscription.delete()
    except NewsletterSubscription.DoesNotExist:
        pass
    return HttpResponse()


def unsubscribe(request, hashed_email):
    context = {"hashed_email": hashed_email}
    return render(request, "tailorscoop/unsubscribe.html", context)


def log_click_and_redirect(request, encoded_url, hashed_email):
    original_url = base64.urlsafe_b64decode(encoded_url).decode("utf-8")

    # Log the click in the database
    click_log = ClickLog(url=original_url, hashed_email=hashed_email)
    click_log.save()

    # Redirect the user to the original source
    return HttpResponseRedirect(original_url)
