from django.dispatch import Signal

message_received = Signal(providing_args=["message"])
