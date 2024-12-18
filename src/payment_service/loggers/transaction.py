from commons import CustomerData, PaymentData, PaymentResponse


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
