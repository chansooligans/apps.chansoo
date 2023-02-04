.PHONY: restart-apache-server django-dev

restart-apache-server:
	sudo /opt/bitnami/ctlscript.sh restart apache

django-dev:
	cd jerseyproj \
	&& python manage.py runserver 0.0.0.0:8000 --settings=settings.dev