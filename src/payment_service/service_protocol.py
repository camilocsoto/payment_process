""" Decorator pattern ☯️
service_protocol.py: Este módulo está dedicado al decorator pattern
paso 1: crear una interfaz o abstracción que describa el comportamiento de PaymentService. (service_protocol.py)
paso 2: hacer que la clase principal implemente la interfaz (service.py)
paso 3: crear una clase decoradora abstracta que implemente la clase principal (decorator_protocol.py)
paso 4: crear una clase concreta que herede de la clase decoradora abstracta (logging_service .py)
paso 5: se crea la lógica que envuelve la lógica original de la clase principal.(decorator_protocol.py)

observer pattern ♾️
Este módulo contiene una implementación Listener, estas son parte de la implementación del patrón observer.
"""

from typing import Protocol
from typing import Optional

from commons import CustomerData, PaymentData, PaymentResponse
from loggers import TransactionLogger
from notifiers import NotifierProtocol
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol,
)
from listeners import ListenersManager
from validators import ChainHandler


class PaymentServiceProtocol(Protocol): #☯️
    """_summary_
    Args:
        Protocol (_type_): interfaz que define el comportamiento de PaymentService.
        no define ningún comportamiento.
    este protocolo lo va a heredar la clase PaymentService. (service.py)
    """
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    validators: ChainHandler
    logger: TransactionLogger
    listeners: Optional[ListenersManager] = None #♾️
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str): ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ): ...
