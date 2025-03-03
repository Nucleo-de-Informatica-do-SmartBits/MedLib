import os, django #noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter #noqa
from channels.security.websocket import AllowedHostsOriginValidator #noqa
from channels.auth import AuthMiddlewareStack #noqa
from django.core.asgi import get_asgi_application #noqa

from library.routing import urlpatterns as websocket_urlpatterns #noqa


dj_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": dj_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
