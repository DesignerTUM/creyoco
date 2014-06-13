import asyncio

from django.core.management import BaseCommand

from django_autobahn.wamp import SimpleServer
from django_autobahn.helpers import run_router


class Command(BaseCommand):
    help = "Run autobahn server on localhost:8080"

    def handle(self, *args, **kwargs):
        coroutine = run_router(SimpleServer)
        loop = asyncio.get_event_loop()
        server = loop.run_until_complete(coroutine)
        server.run_forever()
