# Celery Redis

These commands start Redis, the Celery worker, and the Celery beat processes.
The Celery worker will process tasks, and the Celery beat will schedule tasks to
run periodically based on your settings.


```
redis-server
celery -A apps worker --loglevel=info
celery -A apps beat --loglevel=info 
```

```
python manage.py makemigrations --settings=settings.prod
python manage.py migrate --settings=settings.prod
```