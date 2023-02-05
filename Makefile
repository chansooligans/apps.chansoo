.PHONY: restart-apache-server django-dev collect-static

restart-apache-server:
	sudo /opt/bitnami/ctlscript.sh restart apache

django-dev:
	cd jerseyproj \
	&& python manage.py runserver 0.0.0.0:8000 --settings=settings.dev

collect-static:
	cd jerseyproj \
	&& python manage.py collectstatic --noinput