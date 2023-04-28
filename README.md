# apps.chansoos.com

Hosts:

- https://apps.chansoos.com/centraljersey
    - does "Central Jersey" exist???
- api for personal reminder tool endpoint

To run:

```
cd apps && python manage.py collectstatic --settings=apps.settings.prod --no-input
cd apps && python manage.py runserver --settings=apps.settings.prod
sudo /opt/bitnami/ctlscript.sh restart apache
```
