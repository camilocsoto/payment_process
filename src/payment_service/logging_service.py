"""_summary_
patrón de diseño decorator: ☯️
paso 4: se crea una instancia concreta del objecto a crear, 
"""
from decorator_protocol import PaymentServiceDecoratorProtocol
from service_protocol import PaymentServiceProtocol
from dataclasses import dataclass
from commons import CustomerData, PaymentData, PaymentResponse

@dataclass # ayuda a instanciar la interfaz de wrapped con atributos de datoss
class PaymentServiceLogging(PaymentServiceDecoratorProtocol):
    wrapped: PaymentServiceProtocol # paso 1: interfaz que describe el comportamiento de PaymentService. (service_protocol.py)
    
    """_summary_
    Args:
        PaymentServiceDecoratorProtocol (_type_): clase que hereda de PaymentServiceProtocol
        tiene los mismos métodos de PaymentService
    Do:
        Agregar lógica que decora la clase principal PaymentService sin modificar la lógica existente. ☯️
    Return:
        None
    """
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: 
        # add comments for logs
        print("sys has started online transaction")
        response =self.wrapped.process_transaction(customer_data=customer_data,payment_data=payment_data) #☯️
        print("finished online transaction")
        return response
    def process_refund(self, transaction_id: str):
        print(f"start refund process {transaction_id}")
        response =self.wrapped.process_refund(transaction_id) #☯️
        print(f"finished refund process {transaction_id}")
        return response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData): 
        print("start recurring process")
        response =self.wrapped.setup_recurring(customer_data=customer_data, payment_data=payment_data) #☯️
        print("finished recurring process")
        return response

    
    