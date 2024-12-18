from commons import PaymentData, PaymentType

from processors import (
    PaymentProcessorProtocol,
    OfflinePaymentProcessor,
    StripePaymentProcessor,
    LocalPaymentProcessor,
)


class PaymentProcessorFactory:
    @staticmethod
    def create_payment_processor(
        payment_data: PaymentData,
    ) -> PaymentProcessorProtocol:
        match payment_data.type:
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor()

            case PaymentType.ONLINE:
                match payment_data.currency:
                    case "USD":
                        return StripePaymentProcessor()
                    case _:
                        return LocalPaymentProcessor()

            case _:
                raise ValueError("No se Soporta este tipo de pago")
