"""
Este archivo tendrá la lógica de negocio, la implementación de los protocolos de alto nivel
"""
from loggers import TransactionLogger
from notifiers import EmailNotifier
from processors import StripePaymentProcessor
from service import PaymentService
from validators import CustomerValidator, PaymentDataValidator

if __name__ == "__main__":
    stripe_pay_processor = StripePaymentProcessor()
    mail_notifier = EmailNotifier()
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()
    service = PaymentService(
        payment_processor=stripe_pay_processor, 
        notifier=mail_notifier, 
        validators= customer_validator, 
        payment_validator =payment_data_validator,
        logger=logger
    
    )
    # stripe_payment_processor = StripePaymentProcessor()

    # notifier = get_notifier_implementation(customer_data=customer_data)

    # email_notifier = get_email_notifier()
    # sms_notifier = get_sms_notifier()

    # customer_validator = CustomerValidator()
    # payment_data_validator = PaymentDataValidator()
    # logger = TransactionLogger()
    ...