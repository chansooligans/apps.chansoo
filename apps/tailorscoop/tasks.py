from celery import shared_task
from tailoredscoop.news import api
from tailoredscoop.documents import summarize
from django.core.mail import send_mail
from tailoredscoop import config
import openai
from tailorscoop.models import NewsletterSubscription
import hashlib
import datetime
from pymongo.errors import DuplicateKeyError

class NewsletterSender:

    def save_summary(self, news_downloader, date, hash, kw=None):
        if kw:
            articles = news_downloader.query_news_by_topic(kw)
        else:
            articles = news_downloader.get_top_news()
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
        print(subscribed_users)

        now = datetime.datetime.now()
    
        # Send emails to subscribed users
        for user in subscribed_users:
            print(user)
            
            if user.keywords != "":
                summary_hash = hashlib.sha256((user.keywords + now.strftime("%Y-%m-%d %H")).encode()).hexdigest()
            else:
                summary_hash = hashlib.sha256((now.strftime("%Y-%m-%d %H")).encode()).hexdigest()
            
            print("get summaries")
            if news_downloader.db.summaries.find_one({"summary_id": summary_hash}):
                print('used cached summary')
                summary = news_downloader.db.summaries.find_one({"summary_id": summary_hash})["summary"]
            else:
                summary = self.save_summary(news_downloader, now, summary_hash, kw=user.keywords)

            print("send emails")
            send_mail(
                subject="Today's Tailored Scoop",
                message=summary,
                from_email="chansoosong@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        print('Successfully sent daily newsletter')


@shared_task(name="send_daily_newsletter")
def send_daily_newsletter():
    command = NewsletterSender()
    command.handle()
