import asyncio

from autobahn.asyncio import wamp

from django_autobahn.signals import message_received


class SimpleServer(wamp.ApplicationSession):
    """Tracks open nodes and notifies new users"""

    def onConnect(self):
        self.join("creyoco")

    def onJoin(self, details):
        pass

    def onDisconnect(self):
        pass


class SignalServer(wamp.ApplicationSession):
    """Waits on signals and sends them"""

    def onConnect(self):
        self.join("creyoco")

    @asyncio.coroutine
    def onJoin(self, details):
        print("Joined realm")
        def received_callback(message):
            message_received.send(sender=self.__class__, message=message)

        yield from self.subscribe(received_callback, "com.dautobahn.message")
