import asyncio

from autobahn.asyncio import wamp


class SimpleSession(wamp.ApplicationSession):
    """Tracks open nodes and notifies new users"""

    def onConnect(self):
        self.join("creyoco")

    def onJoin(self, details):
        counter = 0
        while True:
            self.publish('com.dautobahn.message', counter)
            counter += 1
            yield from asyncio.sleep(1)

    def onDisconnect(self):
        pass


class SignalSession(wamp.ApplicationSession):
    """Waits on signals and sends them"""
    signal = None
    channel = ""

    def onConnect(self):
        print("Connected")
        self.join("creyoco")

    @asyncio.coroutine
    def onJoin(self, details):
        print("Joined realm")

        def received_callback(message):
            self.signal.send(sender=self.__class__, message=message)

        print("Subscribing to %s with signal %s" % (self.channel, self.signal))
        yield from self.subscribe(received_callback,
                                  "com.dautobahn.%s" % self.channel)
