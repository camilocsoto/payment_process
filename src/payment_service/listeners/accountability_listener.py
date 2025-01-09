"""_summary_
    - Implementación de patrón observer: ♾️
    Do:
        Implementación concreta de un objeto Listener que notifica un pago existoso
        hacia el sistema de contabilidad
        
    
"""

from .listener import Listener


class AccountabilityListener[T](Listener):
    def notify(self, event: T):
        print(f"Notificando el evento {event}")
