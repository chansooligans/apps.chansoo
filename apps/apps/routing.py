from channels.routing import ProtocolTypeRouter, URLRouter
from themind import routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(routing.websocket_urlpatterns)
})
