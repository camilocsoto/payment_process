import os
from dataclasses import dataclass, field
from typing import Optional, Protocol
import uuid
import stripe
from dotenv import load_dotenv
from pydantic import BaseModel
from stripe.error import StripeError

_ = load_dotenv()


class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: Optional[str] = None


class PaymentData(BaseModel):
    amount: int
    source: str


class PaymentResponse(BaseModel):
    status: str
    amount: int
    transaction_id: Optional[str] = None
    message: Optional[str] = None


class PaymentProcessorProtocol(Protocol):
    """
    Protocol for processing payments, refunds, and recurring payments.

    This protocol defines the interface for payment processors. Implementations
    should provide methods for processing payments, refunds, and setting up recurring payments.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...


class RefundPaymentProtocol(Protocol):
    def refund_payment(self, transaction_id: str) -> PaymentResponse: ...


class RecurringPaymentProtocol(Protocol):
    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...


class StripePaymentProcessor(
    PaymentProcessorProtocol, RefundPaymentProtocol, RecurringPaymentProtocol
):
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        try:
            charge = stripe.Charge.create(
                amount=payment_data.amount,
                currency="usd",
                source=payment_data.source,
                description="Charge for " + customer_data.name,
            )
            print("Payment successful")
            return PaymentResponse(
                status=charge["status"],
                amount=charge["amount"],
                transaction_id=charge["id"],
                message="Payment successful",
            )
        except StripeError as e:
            print("Payment failed:", e)
            return PaymentResponse(
                status="failed",
                amount=payment_data.amount,
                transaction_id=None,
                message=str(e),
            )

    def refund_payment(self, transaction_id: str) -> PaymentResponse:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        try:
            refund = stripe.Refund.create(charge=transaction_id)
            print("Refund successful")
            return PaymentResponse(
                status=refund["status"],
                amount=refund["amount"],
                transaction_id=refund["id"],
                message="Refund successful",
            )
        except StripeError as e:
            print("Refund failed:", e)
            return PaymentResponse(
                status="failed",
                amount=0,
                transaction_id=None,
                message=str(e),
            )

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        price_id = os.getenv("STRIPE_PRICE_ID", "")
        try:
            customer = self._get_or_create_customer(customer_data)

            payment_method = self._attach_payment_method(
                customer.id, payment_data.source
            )

            self._set_default_payment_method(customer.id, payment_method.id)

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {"price": price_id},
                ],
                expand=["latest_invoice.payment_intent"],
            )

            print("Recurring payment setup successful")
            amount = subscription["items"]["data"][0]["price"]["unit_amount"]
            return PaymentResponse(
                status=subscription["status"],
                amount=amount,
                transaction_id=subscription["id"],
                message="Recurring payment setup successful",
            )
        except StripeError as e:
            print("Recurring payment setup failed:", e)
            return PaymentResponse(
                status="failed",
                amount=0,
                transaction_id=None,
                message=str(e),
            )

    def _get_or_create_customer(
        self, customer_data: CustomerData
    ) -> stripe.Customer:
        """
        Creates a new customer in Stripe or retrieves an existing one.
        """
        if customer_data.customer_id:
            customer = stripe.Customer.retrieve(customer_data.customer_id)
            print(f"Customer retrieved: {customer.id}")
        else:
            if not customer_data.contact_info.email:
                raise ValueError("Email required for subscriptions")
            customer = stripe.Customer.create(
                name=customer_data.name, email=customer_data.contact_info.email
            )
            print(f"Customer created: {customer.id}")
        return customer

    def _attach_payment_method(
        self, customer_id: str, payment_source: str
    ) -> stripe.PaymentMethod:
        """
        Attaches a payment method to a customer.
        """
        payment_method = stripe.PaymentMethod.retrieve(payment_source)
        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer_id,
        )
        print(
            f"Payment method {payment_method.id} attached to customer {customer_id}"
        )
        return payment_method

    def _set_default_payment_method(
        self, customer_id: str, payment_method_id: str
    ) -> None:
        """
        Sets the default payment method for a customer.
        """
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id,
            },
        )
        print(f"Default payment method set for customer {customer_id}")


class OfflinePaymentProcessor(PaymentProcessorProtocol):
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Processing offline payment for", customer_data.name)
        return PaymentResponse(
            status="success",
            amount=payment_data.amount,
            transaction_id=str(uuid.uuid4()),
            message="Offline payment success",
        )


class Notifier(Protocol):
    """
    Protocol for sending notifications.

    This protocol defines the interface for notifiers. Implementations
    should provide a method `send_confirmation` that sends a confirmation
    to the customer.
    """

    def send_confirmation(self, customer_data: CustomerData): ...


class EmailNotifier:
    def send_confirmation(self, customer_data: CustomerData):
        from email.mime.text import MIMEText

        if not customer_data.contact_info.email:
            raise ValueError("Email address is requiered to send an email")

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email

        print("Email sent to", customer_data.contact_info.email)


@dataclass
class SMSNotifier:
    gateway: str

    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        if not phone_number:
            print("No phone number provided")
            return
        print(
            f"SMS sent to {phone_number} via {self.gateway}: Thank you for your payment."
        )


class TransactionLogger:
    def log_transaction(
        self,
        customer_data: CustomerData,
        payment_data: PaymentData,
        payment_response: PaymentResponse,
    ):
        with open("transactions.log", "a") as log_file:
            log_file.write(
                f"{customer_data.name} paid {payment_data.amount}\n"
            )
            log_file.write(f"Payment status: {payment_response.status}\n")
            if payment_response.transaction_id:
                log_file.write(
                    f"Transaction ID: {payment_response.transaction_id}\n"
                )
            log_file.write(f"Message: {payment_response.message}\n")

    def log_refund(
        self, transaction_id: str, refund_response: PaymentResponse
    ):
        with open("transactions.log", "a") as log_file:
            log_file.write(
                f"Refund processed for transaction {transaction_id}\n"
            )
            log_file.write(f"Refund status: {refund_response.status}\n")
            log_file.write(f"Message: {refund_response.message}\n")


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


class PaymentDataValidator:
    def validate(self, payment_data: PaymentData):
        if not payment_data.source:
            print("Invalid payment data: missing source")
            raise ValueError("Invalid payment data: missing source")
        if payment_data.amount <= 0:
            print("Invalid payment data: amount must be positive")
            raise ValueError("Invalid payment data: amount must be positive")


@dataclass
class PaymentService:
    payment_processor: PaymentProcessorProtocol
    notifier: Notifier
    customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator
    logger: TransactionLogger
    recurring_processor: Optional[RecurringPaymentProtocol] = None
    refund_processor: Optional[RefundPaymentProtocol] = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        self.customer_validator.validate(customer_data)
        self.payment_validator.validate(payment_data)
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
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


if __name__ == "__main__":
    stripe_processor = StripePaymentProcessor()
    offline_processor = OfflinePaymentProcessor()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier(gateway="CustomGateway")
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    logger = TransactionLogger()

    payment_service = PaymentService(
        payment_processor=stripe_processor,
        notifier=email_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
        recurring_processor=stripe_processor,
        refund_processor=stripe_processor,
    )

    second_service = PaymentService(
        payment_processor=offline_processor,
        notifier=sms_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
    )
