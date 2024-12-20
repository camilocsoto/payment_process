""" Principio solid O
- Permite agregar más procesadores de pago pero no modificar los existentes
- Permite agregar más notificadores a parte de mail y sms pero no modificar 
los existentes
usa el principio de abstracción y herencia
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from abc import ABC, abstractmethod
import stripe
from dotenv import load_dotenv 
from pydantic import BaseModel
from stripe import Charge
from stripe.error import StripeError

_ = load_dotenv()

class ContactInfo(BaseModel):
    # Optional is an object from typing library and its type is str,
    # but for default it's null.
    email: Optional[str] = None
    phone: Optional[str] = None

class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo

class PaymentData(BaseModel):
    amount: int
    source: str


@dataclass
class CustomerValidator:
    def validate(self, customer_data: CustomerData):
        if not customer_data.name:
            print("Invalid customer data: missing name")
            raise ValueError("Invalid customer data: missing name")
        if not customer_data.contact_info:
            print("Invalid customer data: missing contact info")
            raise ValueError("Invalid customer data: missing contact info")
        if not (
            customer_data.contact_info.email
            or customer_data.contact_info.phone
        ):
            print("Invalid customer data: missing email and phone")
            raise ValueError("Invalid customer data: missing email and phone")


@dataclass
class PaymentDataValidator:
    def validate(self, payment_data: PaymentData):
        if not payment_data.source:
            print("Invalid payment data: missing source")
            raise ValueError("Invalid payment data: missing source")
        if payment_data.amount <= 0:
            print("Invalid payment data: amount must be positive")
            raise ValueError("Invalid payment data: amount must be positive")

class Notifier(ABC): # interface
    @abstractmethod
    def send_confirmation(self, customer_data: CustomerData): ...


class EmailNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        from email.mime.text import MIMEText

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email or ""

        print("Email sent to", customer_data.contact_info.email)


class SMSNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        sms_gateway = "the custom SMS Gateway"
        print(
            f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
        )


@dataclass
class TransactionLogger:
    def log(
        self,
        customer_data: CustomerData,
        payment_data: PaymentData,
        charge: Charge,
    ):
        with open("transactions.log", "a") as log_file:
            log_file.write(
                f"{customer_data.name} paid {payment_data.amount}\n"
            )
            log_file.write(f"Payment status: {charge['status']}\n")


class PaymentProcessor(ABC):
    @abstractmethod
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge: ... # la lógica la implementan los procesadores (subclases)

"""
# Al compilar, no se debe ejecutar a StripePaymentProcessor (subclase), sino que debe 
# ejecutarse a PaymentProcessor (la interface o clase abstracta) en el __name__
"""

@dataclass
class StripePaymentProcessor(PaymentProcessor):
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        try:
            charge = stripe.Charge.create(
                amount=payment_data.amount,
                currency="usd",
                source=payment_data.source,
                description="Charge for " + customer_data.name,
            )
            print("Payment successful")
            return charge
        except StripeError as e:
            print("Payment failed:", e)
            raise e


@dataclass
class PaymentService: # orquesta todas las clases
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    """
    # no uses StripePaymentProcessor, usa la clase abstracta o intermedia,
    # asi no dependes de los métodos de stripe, sino de una clase abstracta.
    ----------------------------------------------------------------------
    si dejáses: payment_processor: PaymentProcessor, funcionaría. Pero la clase abs. no tiene
    ninguna lógica, por lo que solo recibiría la info el objeto de tipo PaymentProcessor
    # la lógica la tiene el procesador de pagos de stripe.
    # field() es un atributo del dataclass.
    # default_factory crea por defecto a StripePaymentProcessor como instancia de la clase.
    """
    payment_processor: PaymentProcessor = field( 
        default_factory=StripePaymentProcessor
    )
    notifier: Notifier = field(default_factory=EmailNotifier)
    logger = TransactionLogger()

    def process_transaction(self, customer_data, payment_data) -> Charge:
        try:
            self.customer_validator.validate(customer_data)
        except ValueError as e:
            raise e

        try:
            self.payment_validator.validate(payment_data)
        except ValueError as e:
            raise e

        try:
            charge = self.payment_processor.process_transaction(
                customer_data, payment_data
            )
            self.notifier.send_confirmation(customer_data, payment_data)
            self.logger.log(customer_data, payment_data, charge)
            return charge
        except StripeError as e:
            raise e

if __name__ == "__main__":
    #evita que por defecto se envíe al mail y se envía al sms
    sms_notifier = SMSNotifier()
    payment_processor = PaymentService(notifier=SMSNotifier)

    customer_data_with_email = CustomerData(
        name="John Doe", contact_info=ContactInfo(email="john@example.com")
    )
    customer_data_with_phone = CustomerData(
        name="John Doe", contact_info=ContactInfo(phone="1234567890")
    )

    payment_data = PaymentData(amount=100, source="tok_visa")

    payment_processor.process_transaction( 
        customer_data_with_email, payment_data
    )
    payment_processor.process_transaction(
        customer_data_with_phone, payment_data
    )

    try:
        error_payment_data = PaymentData(amount=100, source="tok_radarBlock")
        payment_processor.process_transaction(
            customer_data_with_email, error_payment_data
        )
    except Exception as e:
        print(f"Payment failed and PaymentProcessor raised an exception: {e}")
