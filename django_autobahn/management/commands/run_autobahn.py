import asyncio

from django.core.management import BaseCommand

from django_autobahn.wamp import SimpleSession
from django_autobahn.helpers import run_router


class Command(BaseCommand):
    help = "Run autobahn server on localhost:8080"

    def handle(self, *args, **kwargs):
        run_router(SimpleSession)
        asyncio.get_event_loop().run_forever()
