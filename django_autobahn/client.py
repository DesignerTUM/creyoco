from django_autobahn.helpers import run_client
from django_autobahn.wamp import SignalSession


def start_clients():
    run_client(SignalSession)
