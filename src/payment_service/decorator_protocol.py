"""_summary_
3 punto: Este módulo contiene la abstracción de los decoradores que van 
a agregar funcionalidades a la clase principal PaymentService.
"""
from typing import Protocol
from service_protocol import PaymentServiceProtocol


from commons import CustomerData, PaymentData, PaymentResponse


class PaymentServiceDecoratorProtocol(Protocol):
    wrapped: PaymentServiceProtocol
    # esta clase necesita los mismos métodos de PaymentServiceProtocol, para cumplir con el principio L y que no genere errores
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str): ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ): ...
