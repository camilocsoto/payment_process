import os

import stripe
from dotenv import load_dotenv
from stripe.error import StripeError  # type: ignore

from commons import CustomerData, PaymentData, PaymentResponse

from .payment import PaymentProcessorProtocol
from .recurring import RecurringPaymentProcessorProtocol
from .refunds import RefundProcessorProtocol

_ = load_dotenv()


class StripePaymentProcessor(
    PaymentProcessorProtocol,
    RefundProcessorProtocol,
    RecurringPaymentProcessorProtocol,
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
