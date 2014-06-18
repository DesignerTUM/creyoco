from functools import wraps

from django.dispatch import Signal, receiver

from django_autobahn.helpers import run_client
from django_autobahn.wamp import SignalSession


message_received = Signal(providing_args=["message"])


class SignalRegistrant:
    """
    Tracks signal registered with Django Autobahn
    """

    def __init__(self):
        self.signals = {}
        self.clients = []

    def register_signal(self, name):
        """
        Register a new signal handler with name *name*
        """
        self.signals[name] = signal = Signal(providing_args=['message'])
        self.clients.append(
            type(
                "SignalSessionWrapper",
                (SignalSession,),
                {"channel": name, "signal": signal}
            )
        )

    def receiver(self, signal_name):
        """
        A wrapper for django.dispatch.receiver. Takes a signal name which
        has to be registered already.
        """
        receiver_wrapper = receiver(signal=self.signals[signal_name])

        @wraps(receiver_wrapper)
        def wrapper(func):
            return receiver_wrapper(func)

        return wrapper

    def receiver_new(self, signal_name):
        """
        Combines SignalRegistrant.register_signal and SignalRegistrant.receiver.
        signal_name must not be registered yet.
        """
        assert not signal_name in self.signals, \
            "%s already registered, use @SignalRegistrant.receiver instead"
        self.register_signal(signal_name)
        return self.receiver(signal_name)

    def run_clients(self):
        """
        Creates connections for the registered clients
        """
        for client in self.clients:
            run_client(client)

signal_registrant = SignalRegistrant()
