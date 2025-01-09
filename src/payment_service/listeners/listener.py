"""_summary_
Implementación de patrón observer: ♾️
paso 1: declarar la interfaz que va a definir la forma del listener (listener.py)
paso 2: declara la clase manejadora de listeners (manager.py)
paso 3: crea una clase concreta que implemente la interfaz Listener (accountability_listener.py)
paso 4: modificar la clase principal para que ahora contenga el atributo Listener (service_protocol.py - factory.py - builder.py)
"""

from typing import Protocol


class Listener[T](Protocol): # recibe cualquier tipo de dato, no necesita una estructura específica
    # método de alto nivel que define la lógica de negocio
    def notify(self, event: T): ...
