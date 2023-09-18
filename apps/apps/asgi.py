"""
ASGI config for apps project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import sys
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

sys.path.append('/home/bitnami/projects/apps.chansoo')
sys.path.append('/home/bitnami/projects/apps.chansoo/apps')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings.prod')

django_asgi_app  = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app ,
    # Just HTTP for now. (We can add other protocols later.)
})