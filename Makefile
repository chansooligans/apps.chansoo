.PHONY: restart-apache-server django-dev collect-static celery-redis adminer

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

adminer:
	docker run --name adminer --rm -d -p 8101:80 dockette/adminer:full