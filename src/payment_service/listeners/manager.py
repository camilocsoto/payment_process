"""_summary_
Implementación de patrón observer: ♾️
- declara la clase manejadora de listeners para agregar, eliminar y notificar todos los objetos registrados
"""

from dataclasses import dataclass, field
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .listener import Listener



@dataclass
class ListenersManager[T]:
    # Args: se refiere a todos los objetos que implementan la interfaz Listener
    listeners: list[Listener] = field(default_factory=list)
    #con field(default_factory=list) se inicializa como una lista vacía, es decir, 
    # que no generaría error por dejar la clase sin argumentos.

    def subscribe(self, listener: Listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener: Listener):
        self.listeners.remove(listener)

    def notifyAll(self, event: T): # el listener recibe un evento tipo T. Por lo que este también debe.
        for listener in self.listeners:
            listener.notify(event)
