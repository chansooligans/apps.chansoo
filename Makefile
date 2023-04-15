.PHONY: restart-apache-server django-dev collect-static celery-redis

restart-apache-server:
	sudo /opt/bitnami/ctlscript.sh restart apache

django-dev:
	cd apps \
	&& python manage.py runserver 0.0.0.0:8000 --settings=settings.dev

collect-static:
	cd apps \
	&& python manage.py collectstatic --settings=settings.prod --no-input

celery-redis:
	docker-compose up