from dataclasses import dataclass
from decorator_protocol import PaymentServiceDecoratorProtocol
from service_protocol import PaymentServiceProtocol


from commons import CustomerData, PaymentData, PaymentResponse


@dataclass
class PaymentServiceLogging(PaymentServiceDecoratorProtocol):
    wrapped: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Start process transaction")

        response = self.wrapped.process_transaction(
            customer_data, payment_data
        )
        print("Finish process transaction")
        return response

    def process_refund(self, transaction_id: str):
        print(f"Start process refund using: {transaction_id}")

        response = self.wrapped.process_refund(transaction_id)

        print("Finish process refund")
        return response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        print("Start setup recurring")

        print("Finish process refund")
