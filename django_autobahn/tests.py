import asyncio

from django.test import TestCase
from django.dispatch import receiver
from autobahn.asyncio import wamp

from django_autobahn.helpers import run_client, run_router
from django_autobahn.wamp import SimpleServer, SignalServer
from django_autobahn.signals import message_received


class TestServerCommand(TestCase):
    """Basic tests for autobahn server management command"""

    def test_basic_command(self):
        """Create a subscriber and connect to it"""
        connected = False
        loop = asyncio.get_event_loop()
        server = run_router(SimpleServer)

        class SimpleClient(wamp.ApplicationSession):
            def onConnect(self):
                nonlocal connected
                connected = True
                self.disconnect()


        run_client(SimpleClient)
        loop.run_until_complete(asyncio.sleep(.5))
        self.assertTrue(connected)
        server.close()
        asyncio.get_event_loop().stop()


    def test_message_singnal(self):
        """Tests message dispatching"""
        loop = asyncio.get_event_loop()
        server = run_router(SignalServer)
        message = "hello"
        channel = "com.dautobahn.message"
        received = False

        class SendingClient(wamp.ApplicationSession):
            """Sends a message and closes"""
            def onConnect(self):
                self.join("creyoco")
            def onJoin(self, details):
                self.publish(channel, message)
                self.disconnect()

        @receiver(message_received)
        def handle_received(sender, **kwargs):
            nonlocal received
            received = True
            if kwargs['message'] == message:
                received = True
        run_client(SendingClient)
        loop.run_until_complete(asyncio.sleep(.5))
        self.assertTrue(received)
        server.close()
        loop.stop()
