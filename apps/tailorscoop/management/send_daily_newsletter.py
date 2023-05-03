from tailoredscoop.news import api
from tailoredscoop import config
from tailoredscoop.documents import summarize
import openai
from django.core.mail import send_mail
from tailoredscoop.models import NewsletterSubscription

secrets = config.setup()
openai.api_key = secrets["openai"]["api_key"]
news_downloader = api.NewsAPI(api_key=secrets["newsapi"]["api_key"])

# Fetch all subscribed users from the database
subscribed_users = NewsletterSubscription.objects.all()

# Check if there are articles to fetch based on keywords
keywords = ""
if subscribed_users.filter(keywords__isnull=False).exists():
    # Fetch articles based on the common keywords
    articles = news_downloader.query_news_by_topic(keywords)
    res = news_downloader.process(articles, summarizer=summarize.summarizer)
    summary = summarize.get_openai_summary(res)
else:
    # Use the cached summary if no keywords are specified
    summary = "Cached summary for articles without keywords."

# Send emails to subscribed users
for user in subscribed_users:
    # Customize the email message based on user's preferences
    if user.keywords:
        # Fetch articles based on user's keywords
        articles = news_downloader.query_news_by_topic(user.keywords)
        res = news_downloader.process(articles, summarizer=summarize.summarizer)
        user_summary = summarize.get_openai_summary(res)
    else:
        # Use the cached summary for users without keywords
        user_summary = summary

    send_mail(
        subject="Today's Tailored Scoop",
        message=user_summary,
        from_email="chansoosong@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )
