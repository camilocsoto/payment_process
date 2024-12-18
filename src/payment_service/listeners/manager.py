from dataclasses import dataclass, field
from .listener import Listener


@dataclass
class ListenersManager[T]:
    listeners: list[Listener] = field(default_factory=list)

    def subscribe(self, listener: Listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener: Listener):
        self.listeners.remove(listener)

    def notifyAll(self, event: T):
        for listener in self.listeners:
            listener.notify(event)
