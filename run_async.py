#!/usr/bin/env python3
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'exedjango.settings'
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from exedjango.wsgi import application
from django_autobahn.signals import signal_registrant
from django.conf import settings

deployment = False

def run():
    """
    Monkey patch the standard wsgi server
    """
    wsgi_handler = WSGIHandler(application)

    app = web.Application()
    if not deployment:
        app.router.add_static(settings.STATIC_URL, settings.STATIC_ROOT, follow_symlinks=True)
        app.router.add_static(settings.MEDIA_URL, settings.MEDIA_ROOT, follow_symlinks=True)
    app.router.add_route("*", "/{path_info:.*}", wsgi_handler)
    signal_registrant.run_clients()
    web.run_app(app)

if __name__ == "__main__":
    run()