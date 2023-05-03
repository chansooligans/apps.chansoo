.PHONY: restart-apache-server django-dev collect-static celery-redis

restart-apache-server:
	sudo /opt/bitnami/ctlscript.sh restart apache

django-dev:
	cd apps \
	&& python manage.py runserver 0.0.0.0:8000 --settings=apps.settings.dev

collect-static:
	cd apps \
	&& python manage.py collectstatic --settings=apps.settings.prod --no-input

celery-redis:
	docker-compose up

shell_plus:
	cd apps \
	&& ./manage.py shell_plus --ipython --settings=apps.settings.dev