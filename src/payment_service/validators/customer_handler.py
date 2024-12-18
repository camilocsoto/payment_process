from commons.request import Request
from .chain_handler import ChainHandler

from .customer import CustomerValidator


class CustomerHandler(ChainHandler):
    def handle(self, request: Request):
        validator = CustomerValidator()
        try:
            validator.validate(request.customer_data)
            if self._next_handler:
                self._next_handler.handle(request)
        except Exception as e:
            print("error")
            raise e
