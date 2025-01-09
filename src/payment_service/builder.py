"""_summary_
patrón de diseño builder 🔥
paso 1: Usar los mismos atributos de la clase/objeto a construir.
paso 2: Usar Optional y por defecto None para poder construir los objetos paso a paso.
paso 3: Asignar métodos set para cada atributo.
"""
from commons import PaymentData, CustomerData
from typing import Optional, Self
from loggers import TransactionLogger
from notifiers import NotifierProtocol
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol
)
from listeners import ListenersManager, AccountabilityListener
from validators import CustomerHandler, ChainHandler, PaymentDataValidator
from factory import PaymentProcessorFactory, NotifierFactory, RefundPaymentFactory, RecurringPaymentFactory # lógica de elegir cuál procesador de pago usar
from service import PaymentService
class PaymentServiceBuilder:
    """_summary_
    Do:
        Para construir la clase paso a paso, necesita que los atributos sean opcionales original y por defecto None.
        🟥 Se puede instanciar de forma directa porque no necesita de ninguna abstracción. Solo usa métodos set (fácil)
        🟦 Necesita implementar una lógica extra porque depende de abstracciones.
    """
    payment_processor: Optional[PaymentProcessorProtocol] = None # 🟦
    notifier: Optional[NotifierProtocol] = None # 🟦
    validators: Optional[ChainHandler] = None # 🟥
    logger: Optional[TransactionLogger] = None # 🟥
    listeners: Optional[ListenersManager] = None # 🟥
    refund_processor: Optional[RefundProcessorProtocol] = None # 🟦
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None # 🟦
    
    # 🟥
    def setLogger(self) -> Self:
        self.logger = TransactionLogger()
        return self

    def set_payment_validation(self) -> Self:
        handler1 = CustomerHandler()
        handler2 = PaymentDataValidator()
        handler1.set_next(handler2)
        self.validators = handler1
        return self
    
    def set_listener(self) -> Self:
        self.listeners = ListenersManager()
        return self
    
    # 🟦 la lógica de elección está en factory.py
    
    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        """_summary_
        Args:
            payment_data: info de pago y método de pago para elegir cuál usar.
        Do:
            En Factory, se creó la lógica para elegir el procesador de pago.
        Returns:
            Una clase (stripe, local, offline)
        """
        self.payment_processor = PaymentProcessorFactory.create_payment_processor(payment_data)
        return self
    
    def set_notifier(self, customer_data: CustomerData) -> Self:
        """_summary_
        Args:
            customer_data: info de cliente
        Do:
            En Factory, se creó la lógica para elegir el notificador.
        Returns:
            Una clase (sms, email)
        """
        self.notifier = NotifierFactory.create_notifier(customer_data)
        return self
    
    def set_refund_processor(self, transaction_id) -> Self:
        self.refund_processor = RefundPaymentFactory.refundPayment(transaction_id)
        return self
    
    def set_recurring_payment(self, customer_data: CustomerData, payment_data: PaymentData) -> Self:
        self.recurring_processor = RecurringPaymentFactory.setup_recurring(customer_data=customer_data, payment_data=payment_data)
        return self
    
    def set_listener(self) -> Self: # Parte de observer pattern ♾️
        listen = ListenersManager() # generaría error. Ve a manager.py
        account = AccountabilityListener()
        listen.subscribe(account)
        self.listeners = listen        
    
    def build(self):
        #si no están todos los atributos del objeto:
        if not all( # si alguno de los elementos dentro de la lista no existe o es None, retorna False
            [
                self.payment_processor,
                self.notifier,
                self.validators,
                self.listeners,
                self.logger
            ]
        ):
            # la siguiente list_comprenhension guarda los nombres de los atributos que no se han instanciado (value)
            missing = [name for name, value in [("payment", self.payment_processor), ("notifier", self.notifier), ("validators", self.validators), ("logger", self.logger), ("listener", self.listeners)] if value is None]
            raise ValueError(f"Missing dependencies: {missing}")
        return PaymentService( 
            payment_processor= self.payment_processor,
            notifier= self.notifier,
            validators= self.validators,
            logger= self.logger     
        )