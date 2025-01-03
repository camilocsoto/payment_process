"""
Este archivo tendrá la lógica de negocio, la implementación de los protocolos de alto nivel:
- Implementación de patrón strategy. 🆗

"""
from loggers import TransactionLogger
from notifiers import EmailNotifier, SMSNotifier, NotifierProtocol #🆗
from processors import StripePaymentProcessor
from service import PaymentService
from validators import PaymentDataValidator, CustomerHandler
from commons import CustomerData, ContactInfo #🆗

def get_notifier_implementation(customer_data: CustomerData) -> NotifierProtocol:
    """ 🆗 implementación de patrón strategy que escoge el método de notificación
        este método realiza validaciones de campos vacios en mail y phone de customerData
        este método retorna una u otra instancia del protocolo Notifications
    """
    # elije una u otra o ambas estrategias
    if customer_data.contact_info.phone:
        return get_sms()
    
    if customer_data.contact_info.email:
        return get_mail()
    
    raise ValueError("No se puede elegir ningún tipo de estrategia. Ambas están vacias.")

def get_customer_info():
    contactInfo = ContactInfo(email="johndoe.@gmail.com",phone="31966238234")
    customer_info = CustomerData(name="John Doe", contact_info=contactInfo) #🆗 aqui hay un error
    return customer_info
# Las siguientes 2 funciones seleccionan el tipo de proceso: 🆗
def get_sms()-> NotifierProtocol:
    """ it just select the sms notifier processor"""
    return SMSNotifier(gateway="Tigo Processor")

def get_mail()-> NotifierProtocol:
    """ it just select the mail notifier processor"""
    return EmailNotifier

if __name__ == "__main__":
    stripe_pay_processor = StripePaymentProcessor()
    # 🆗 principio S
    customer_data =get_customer_info()
    notifier= get_notifier_implementation(customer_data = customer_data)
    # Para cambiar de estrategia según el contexto parte 1:
    email_notifier = get_mail
    sms_notifier = get_sms()
    
    # Se crea el manejador de dict y configura la cadena de validación
    handler_map = CustomerHandler()
    payment_data_validator = PaymentDataValidator()
    handler_map.set_next(payment_data_validator)
    # Asigna la cadena de validadores a dictionaries_map
    dictionaries_map = handler_map
    
    logger = TransactionLogger()
    
    service = PaymentService( 
        payment_processor=stripe_pay_processor, 
        notifier=notifier, #🆗
        validators= dictionaries_map, 
        logger=logger
    )
    # parte 2: Cambia la estrategia a email: 🆗
    service.set_notifier(EmailNotifier)
    #si falla: escoge la otra estrategia:
    service. set_notifier()