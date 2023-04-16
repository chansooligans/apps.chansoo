# Celery Redis

These commands start Redis, the Celery worker, and the Celery beat processes.
The Celery worker will process tasks, and the Celery beat will schedule tasks to
run periodically based on your settings.

From the apps directory:

```
redis-server
celery -A apps worker --loglevel=info
celery -A apps beat --loglevel=info 
celery -A apps flower  --address=0.0.0.0 --port=5566
```

```
python manage.py makemigrations --settings=apps.settings.prod
python manage.py migrate --settings=apps.settings.prod
```