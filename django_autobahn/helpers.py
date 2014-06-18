"""
Collection of useful autobahn helpers
"""
import asyncio

from autobahn.wamp import router
from autobahn.asyncio import wamp, websocket


def run_client(application_class):
    """Run autobahn application"""

    session_factory = wamp.ApplicationSessionFactory()
    session_factory.session = application_class
    transport_factory = websocket.WampWebSocketClientFactory(session_factory,
                                                             debug=False,
                                                             debug_wamp=False)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        loop.create_connection(transport_factory, '127.0.0.1', 8080)
    )


def run_router(application_class):
    """Run autobahn router as applicaiton"""

    router_factory = router.RouterFactory()
    session_factory = wamp.RouterSessionFactory(router_factory)
    session_factory.add(application_class())
    transport_factory = websocket.WampWebSocketServerFactory(session_factory,
                                                             debug=False,
                                                             debug_wamp=False)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        loop.create_server(transport_factory, '127.0.0.1', 8080)
    )
