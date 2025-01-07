"""
Implementación de patrón strategy: 🆗
Dentro del contexto del notificador.
Pasos:
1. Crear un método que permita cambiar el comportamiento de una clase cuando se esté ejecutando (setNotfier )
2. Crear una función que permita elegir el comportamiendo mientras se ejecuta: si es una clase u otra. (ir a main.py, y busca get_notifier)
nota: revisa el final del archivo main.py, allí se vé como se implementa

Implementación de patrón factory: 🟢
"""
from dataclasses import dataclass
from typing import Optional, Self

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
Tiene agregadOs atributos que NO son funcionalidades concretas. Ej: Notifier, cuando debería ser email o sms
"""
@dataclass
class PaymentService(PaymentServiceProtocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol #🆗
    validators: ChainHandler
    logger: TransactionLogger
    listeners: Optional[ListenersManager] = None
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None

    def set_notifier(self, notifier: NotifierProtocol): #🆗
        """Debe modificar la estrategia: si es por sms o por mail."""
        print("Changing the notifier implementation")
        self.notifier = notifier

    @classmethod
    def create_processor_payment_factory(cls, payment_data: PaymentData,**kwargs) -> Self:
        """_summary_
            info:
                patrón creacional factory: La creación de la clase depende de un objeto tipo payment_data
                encapsula la creación hacia el método factory
            args:
                cls: es la clase local, offline o online.
                payment_data: es el objeto que se va a procesar.
                **kguargs: recibe notifier, customer_validator, payment_data_validator: que son enviadas por
        """
        try:
            # crea una instancia de la clase PaymentProcessorFactory y disperasa la información:
            processor = PaymentProcessorFactory.create_payment_processor(payment_data)
            # retorna la instancia de la misma clase
            return cls(payment_processor=processor, **kwargs)
        except Exception as e: # si ProcessTransaction genera un error, lo crea de tipo valueError
            raise ValueError(f"error al crear el procesador de pago: {e}")
        

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
