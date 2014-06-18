import asyncio

from aiohttp.wsgi import WSGIServerHttpProtocol
from django_autobahn.signals import signal_registrant


def run(addr, port, wsgi_handler, loop=None, **options):
    """
    Monkey patch the standard wsgi server
    """
    print("Creating event loop")
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    protocol_factory = lambda: WSGIServerHttpProtocol(
        wsgi_handler, readpayload=True
    )
    server = loop.run_until_complete(
        loop.create_server(protocol_factory, addr, port)
    )
    signal_registrant.run_clients()

    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())


def patch():
    from django.core.management.commands import runserver
    runserver.run = run
