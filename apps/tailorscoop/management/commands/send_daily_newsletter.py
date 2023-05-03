from django.core.management.base import BaseCommand
from tailoredscoop.news import api
from tailoredscoop.documents import summarize
from django.core.mail import send_mail
from tailoredscoop import config
import openai
from tailorscoop.models import NewsletterSubscription
import hashlib
import datetime

from pymongo.errors import DuplicateKeyError

class Command(BaseCommand):
    help = 'Send daily newsletter to subscribed users'

    def save_summary(self, news_downloader, date, hash, articles):
        res = news_downloader.process(articles, summarizer=summarize.summarizer)
        summary = summarize.get_openai_summary(res)
        summary_obj = {
            "created_at":date,
            "summary_id":hash,
            "summary":summary
        }
        try:
            news_downloader.db.summaries.insert_one(summary_obj)
            print(f"Inserted summary: {hash}")
        except DuplicateKeyError:
            print(f"Summary with URL already exists: {hash}")
        return summary

        
    def handle(self, *args, **options):
        secrets = config.setup()
        openai.api_key = secrets["openai"]["api_key"]
        news_downloader = api.NewsAPI(api_key=secrets["newsapi"]["api_key"])

        # Fetch all subscribed users from the database
        subscribed_users = NewsletterSubscription.objects.all()

        now = datetime.datetime.now()
    
        # Send emails to subscribed users
        for user in subscribed_users:
            
            if user.keywords != "":
                # Fetch articles based on user's keywords
                summary_hash = hashlib.sha256((user.keywords + now.strftime("%Y-%m-%d %H")).encode()).hexdigest()
                articles = news_downloader.query_news_by_topic(user.keywords)
            else:
                # Use the cached summary for users without keywords
                summary_hash = hashlib.sha256((now.strftime("%Y-%m-%d %H")).encode()).hexdigest()
                articles = news_downloader.get_top_news()
            
            if news_downloader.db.summaries.find_one({"summary_id": summary_hash}):
                summary = news_downloader.db.summaries.find_one({"summary_id": summary_hash})["summary"]
            else:
                summary = self.save_summary(news_downloader, now, summary_hash, articles)

            send_mail(
                subject="Today's Tailored Scoop",
                message=summary,
                from_email="chansoosong@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS('Successfully sent daily newsletter'))
