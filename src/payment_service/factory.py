from commons import PaymentData, PaymentType
from processors import PaymentProcessorProtocol, OfflinePaymentProcessor, LocalPaymentProcessor, StripePaymentProcessor
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
        """_summary_
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
            