from loggers import TransactionLogger
from notifiers import EmailNotifier, NotifierProtocol, SMSNotifier
from processors import StripePaymentProcessor
from service import PaymentService
from validators import CustomerValidator, PaymentDataValidator

from builder import PaymentServiceBuilder
from commons import CustomerData, ContactInfo, PaymentData

from logging_service import PaymentServiceLogging


def get_email_notifier() -> EmailNotifier:
    return EmailNotifier()


def get_sms_notifier() -> SMSNotifier:
    return SMSNotifier(gateway="SMSGatewayExample")


def get_notifier_implementation(
    customer_data: CustomerData,
) -> NotifierProtocol:
    if customer_data.contact_info.phone:
        return get_sms_notifier()

    if customer_data.contact_info.email:
        return get_email_notifier()
    raise ValueError("No se puede elegir la estrategia correcta")


def get_customer_data() -> CustomerData:
    contact_info = ContactInfo(email="jon.doe@mail.co")
    customer_data = CustomerData(name="Jon Doe", contact_info=contact_info)

    return customer_data


if __name__ == "__main__":
    # stripe_payment_processor = StripePaymentProcessor()

    customer_data = get_customer_data()
    # notifier = get_notifier_implementation(customer_data=customer_data)

    # email_notifier = get_email_notifier()
    # sms_notifier = get_sms_notifier()

    # customer_validator = CustomerValidator()
    # payment_data_validator = PaymentDataValidator()
    # logger = TransactionLogger()

    payment_data = PaymentData(amount=1500, source="tok_visa", currency="USD")
    builder = PaymentServiceBuilder()
    service = (
        builder.set_logger()
        .set_payment_processor(payment_data)
        .set_chain_of_validations()
        .set_notifier(customer_data)
        .set_listeners()
        .build()
    )

    service.process_transaction(customer_data, payment_data)

    # service = PaymentService.create_with_payment_processor(
    #     payment_data=payment_data,
    #     notifier=notifier,
    #     customer_validator=customer_validator,
    #     payment_validator=payment_data_validator,
    #     logger=logger,
    # )

    # logging_service = PaymentServiceLogging(wrapped=service)

    # logging_service.process_refund(transaction_id="12345")
