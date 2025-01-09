"""
Este archivo tendrá la lógica de negocio, la implementación de los protocolos de alto nivel:
- Implementación de Principio S. 🛸
- Implementación de patrón strategy. 🆗
- Implementación de patrón factory. 🟢
- Implementación de patrón decorator: ☯️


"""
from loggers import TransactionLogger
from notifiers import EmailNotifier, SMSNotifier, NotifierProtocol #🆗
from processors import StripePaymentProcessor
from service import PaymentService
from validators import PaymentDataValidator, CustomerHandler
from commons import CustomerData, ContactInfo, PaymentData #🆗
from logging_service import PaymentServiceLogging #☯️
from builder import PaymentServiceBuilder #🔥

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
    # 🛸 principio S
    customer_data =get_customer_info()
    notifier= get_notifier_implementation(customer_data = customer_data)
    
    # Se crea el manejador de dict y configura la cadena de validación
    handler_map = CustomerHandler()
    payment_data_validator = PaymentDataValidator()
    handler_map.set_next(payment_data_validator)
    # Asigna la cadena de validadores a dictionaries_map
    dictionaries_map = handler_map
    logger = TransactionLogger()
    
    # 🆗 Patrón strategy para cambiar de estrategia según el contexto parte 1:
    email_notifier = get_mail
    sms_notifier = get_sms()
    
    strategy_service = PaymentService( 
        payment_processor=stripe_pay_processor, 
        notifier=notifier, #🆗
        validators= dictionaries_map, 
        logger=logger
    )
    # parte 2: Cambia la estrategia a email: 🆗
    strategy_service.set_notifier(EmailNotifier)
    #si falla: escoge la otra estrategia:
    strategy_service.set_notifier(SMSNotifier)
    
    # Implementación del patrón factory 🟢
    payment_data = PaymentData(amount=100, source="tok_visa" ,currency="USD", type="online") 
     # por defecto type es ONLINE, entonces no sería necesario ponerlo.
    factory_service = PaymentService.create_processor_payment_factory(
        payment_data=payment_data, 
        notifier=notifier, 
        validators= dictionaries_map, 
        logger=logger)
    
    # Implementación de patrón decorator ☯️
    payment_data = PaymentData(amount=100, source="tok_visa" ,currency="USD", type="online") 
     # por defecto type es ONLINE, entonces no sería necesario ponerlo.
    decorator_service = PaymentService.create_processor_payment_factory(
        payment_data=payment_data, 
        notifier=notifier, 
        validators= dictionaries_map, 
        logger=logger)
    loggin_service = PaymentServiceLogging(wrapped=decorator_service)
    
    # Implementación de patrón builder 🔥
    builder = PaymentServiceBuilder()
    payment_data = PaymentData(amount=100, source="tok_visa" ,currency="USD", type="online") 
    builder_service = (
        builder.set_payment_processor(payment_data)
        .set_notifier(customer_data)
        .set_payment_validation()
        .setLogger()
        .build()
    )