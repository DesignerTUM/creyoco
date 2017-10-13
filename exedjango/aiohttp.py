from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from exedjango.wsgi import application
from django_autobahn.signals import signal_registrant
from django.conf import settings


def create_aiohttp_app():
    """
    Monkey patch the standard wsgi server
    """
    wsgi_handler = WSGIHandler(application)

    app = web.Application()
    if not settings.DEBUG:
        app.router.add_static(settings.STATIC_URL, settings.STATIC_ROOT, follow_symlinks=True)
        app.router.add_static(settings.MEDIA_URL, settings.MEDIA_ROOT, follow_symlinks=True)
    app.router.add_route("*", "/{path_info:.*}", wsgi_handler)
    signal_registrant.run_clients()
    return app

app = create_aiohttp_app()