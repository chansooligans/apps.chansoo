# apps.chansoos.com

Uses:

- https://apps.chansoos.com/centraljersey
    - does "Central Jersey" exist???
- https://tailoredscoops.com (i.e. apps.chansoos.com/tailoredscoop)
    - AI-personalized daily newsletter
- api for reminder tool endpoint ("RemindMe", currently only for personal use)

To run:

```
cd apps && python manage.py collectstatic --settings=apps.settings.prod --no-input
cd apps && python manage.py runserver --settings=apps.settings.prod
sudo /opt/bitnami/ctlscript.sh restart apache
```

Reminder for setup:

https://github.com/chansooligans/django/blob/master/lecture_notes/new_project_steps.md


