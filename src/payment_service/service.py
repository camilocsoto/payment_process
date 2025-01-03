"""
Implementación de patrón strategy:
Dentro del contexto del notificador.
Pasos:
1. Crear un método que permita cambiar el comportamiento de una clase cuando se esté ejecutando (setNotfier )
2. Crear una función que permita elegir el comportamiendo mientras se ejecuta: si es una clase u otra. (ir a main.py, y busca get_notifier)
nota: revisa el final del archivo main.py, allí se vé como se implementa
"""
from dataclasses import dataclass
from typing import Optional

from commons import CustomerData, PaymentData, PaymentResponse, Request
from loggers import TransactionLogger
from notifiers import NotifierProtocol
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol
) # trae los 3 protocolos sin una implementación especifica
from validators import CustomerValidator, PaymentDataValidator
from factory import PaymentProcessorFactory


from service_protocol import PaymentServiceProtocol
from listeners import ListenersManager
from validators import ChainHandler


"""
# 🆗 esta clase de alto nivel ahora será una interfaz, mediadora entre la clase abstracta
Tiene agregadas unos atributos que no son funcionalidades concretas. Ej: Notifier, cuando debería ser email o sms
"""
@dataclass
class PaymentService(PaymentServiceProtocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    validators: ChainHandler
    logger: TransactionLogger
    listeners: Optional[ListenersManager] = None
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None

    @classmethod
    def create_with_payment_processor(
        cls, payment_data: PaymentData, **kwargs
    ) -> 'create_with_payment_processor':
        try:
            processor = PaymentProcessorFactory.create_payment_processor(
                payment_data
            )
            return cls(payment_processor=processor, **kwargs)
        except ValueError as e:
            print("Error creando la clase")
            raise e

    def set_notifier(self, notifier: NotifierProtocol): #🆗
        """Debe modificar la estrategia: si es por sms o por mail."""
        print("Changing the notifier implementation")
        self.notifier = notifier

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        try:
            request = Request(
                customer_data=customer_data, payment_data=payment_data
            )
            self.validators.handle(request=request)

        except Exception as e:
            print(f"fallo en las validaciones: {e}")
            raise e
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
        )
        self.listeners.notifyAll(
            f"pago exitoso al evento: {payment_response.transaction_id}"
        )
        self.notifier.send_confirmation(customer_data)
        self.logger.log_transaction(
            customer_data, payment_data, payment_response
        )
        return payment_response

    def process_refund(self, transaction_id: str):
        if not self.refund_processor:
            raise Exception("this processor does not support refunds")
        refund_response = self.refund_processor.refund_payment(transaction_id)
        self.logger.log_refund(transaction_id, refund_response)
        return refund_response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        if not self.recurring_processor:
            raise Exception("this processor does not support recurring")
        recurring_response = self.recurring_processor.setup_recurring_payment(
            customer_data, payment_data
        )
        self.logger.log_transaction(
            customer_data, payment_data, recurring_response
        )
        return recurring_response
