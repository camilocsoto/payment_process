from commons import PaymentData


class PaymentDataValidator:
    def validate(self, payment_data: PaymentData):
        if not payment_data.source:
            print("Invalid payment data: missing source")
            raise ValueError("Invalid payment data: missing source")
        if payment_data.amount <= 0:
            print("Invalid payment data: amount must be positive")
            raise ValueError("Invalid payment data: amount must be positive")
