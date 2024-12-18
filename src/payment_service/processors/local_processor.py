import uuid

from commons import CustomerData, PaymentData, PaymentResponse

from .payment import PaymentProcessorProtocol
from .recurring import RecurringPaymentProcessorProtocol
from .refunds import RefundProcessorProtocol


class LocalPaymentProcessor(
    PaymentProcessorProtocol,
    RefundProcessorProtocol,
    RecurringPaymentProcessorProtocol,
):
    """
    A payment processor that processes payments locally.

    Useful when the payment is not in USD currency.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Processing local payment for", customer_data.name)
        transaction_id = f"local-transaction-id-{uuid.uuid4()}"
        return PaymentResponse(
            status="success",
            amount=payment_data.amount,
            transaction_id=transaction_id,
            message="Local payment success",
        )

    def refund_payment(self, transaction_id: str) -> PaymentResponse:
        print("Processing refund for transaction id", transaction_id)
        return PaymentResponse(
            status="success",
            amount=0,
            transaction_id=transaction_id,
            message="Refund success",
        )

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Setting up recurring payment for", customer_data.name)
        transaction_id = f"local-transaction-id-{uuid.uuid4()}"
        return PaymentResponse(
            status="success",
            amount=payment_data.amount,
            transaction_id=transaction_id,
            message="Recurring payment setup success",
        )
