from .listener import Listener


class AccountabilityListener[T](Listener):
    def notify(self, event: T):
        print(f"Notificando el evento {event}")
