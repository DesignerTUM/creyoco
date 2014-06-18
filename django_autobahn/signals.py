from django.dispatch import Signal, receiver

from django_autobahn.helpers import run_client
from django_autobahn.wamp import SignalSession


message_received = Signal(providing_args=["message"])


class SignalRegistrant:
    def __init__(self):
        self.signals = {}

    def register_signal(self, name):
        self.signals[name] = signal = Signal(providing_args=['message'])
        run_client(
            type(
                "SignalSessionWrapper",
                (SignalSession,),
                {"channel": name, "signal": signal}
            )
        )

    def receiver(self, signal_name):
        def wrapper(func):
            return receiver(signal=self.signals[signal_name])(func)

        return wrapper


signal_registrant = SignalRegistrant()
