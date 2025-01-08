from dataclasses import dataclass
from commons import PaymentData, PaymentType, CustomerData, ContactInfo
from processors import PaymentProcessorProtocol, OfflinePaymentProcessor, LocalPaymentProcessor, StripePaymentProcessor
from service_protocol import PaymentServiceProtocol
from notifiers import NotifierProtocol, EmailNotifier, SMSNotifier
"""_summary_
🟢 El patrón factory encapsula el comportamiendo de clases y utilizar uno u otro para la creación de objetos.
1. File commons/payment_data.py: Se creó la clase PaymentType, que se instancia en el importante PaymentData
2. Se tienen 3 procesadores de pago:
- local_processor: Es online y no usa usd.
- offline_processor: Es offline y no importa la divisa.
- stripe_processor: Es online y usa usd.
"""
class PaymentProcessorFactory():
    
    @staticmethod
    def create_payment_processor(payment_data:PaymentData) -> PaymentProcessorProtocol:
        """
        - Encapsula decisión de cuál procesador de pago tomar
        - el decorador crea un método que no necesita acceso a la instancia (self) ni a la clase (cls). 
        Se utiliza para encapsular funciones que no dependen de los atributos de la clase o de la instancia.
        Args:
            payment_data (PaymentData): Crea un objeto para hacer la transacción.
            En el archivo main.py se observa su intanciamiento.
        """
        match payment_data.type:
            case PaymentType.ONLINE:
                match payment_data.currency:
                    case "USD":
                        return StripePaymentProcessor()
                    case _: #cualquier otra cosa
                        return LocalPaymentProcessor()
                ...
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor() #no hace falta instanciar el método.
            case _: # cualquier otra cosa
                raise ValueError("no se soporta este tipo de pagos")
            

#retos:
class NotifierFactory():
    """_summary_
    Args:
        NotifierProtocol: Interfaz que define el comportamiento de las notificaciones.
        customer_data (CustomerData): Información del cliente.
        ContactInfo: Trae la información de contacto del cliente.
    returns:
        Una instancia de la clase que se va a usar para notificar al cliente.
        
    """
    @staticmethod
    def create_notifier(customer_data:CustomerData) -> NotifierProtocol:

        match customer_data.contact_info:
            case ContactInfo.email:
                return EmailNotifier()
            case ContactInfo.phone: 
                return SMSNotifier(gateway="Tigo_Une: 1234567890")
            case _:
                raise ValueError("no se soporta este tipo de notificación")

@dataclass
class RefundPaymentFactory():
    payment_data: PaymentData
    @staticmethod
    def refundPayment(self, transaction_id:str):
        match self.payment_data.type:
            case PaymentType.ONLINE:
                match self.payment_data.currency:
                    case "USD":
                        return StripePaymentProcessor.refund_payment(transaction_id)
                    case _: #cualquier otra cosa
                        return LocalPaymentProcessor.refund_payment(transaction_id)
                ...
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor() #no hace falta instanciar el método.
            case _: # cualquier otra cosa
                raise ValueError("no se soporta este tipo de reembolsos")
        

class RecurringPaymentFactory():
    @staticmethod
    def setup_recurring(customer_data: CustomerData,payment_data:PaymentData):
        match payment_data.type:
            case PaymentType.ONLINE:
                match payment_data.currency:
                    case "USD":
                        return StripePaymentProcessor.setup_recurring_payment(customer_data, payment_data)
                    case _: #cualquier otra cosa
                        return LocalPaymentProcessor.setup_recurring_payment(customer_data, payment_data)
                ...
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor() #no hace falta instanciar el método.
            case _: # cualquier otra cosa
                raise ValueError("no se soporta este tipo de pagos recurrentes")
        