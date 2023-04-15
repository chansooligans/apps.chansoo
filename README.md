# Is Central Jersey Real?

Testing AWS Lightsail + Django while attempting to resolve a heated dispute 
among friends and family centered on the question: does "Central Jersey" 
exist???

See app on https://apps.chansoos.com/centraljersey

To run:

```
python manage.py collectstatic --settings=settings.prod --no-input
sudo /opt/bitnami/ctlscript.sh restart apache
```
