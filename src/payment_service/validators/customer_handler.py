"""_summary_
    #Este archivo es parte de chain of responsability pattern ☣️
"""

from commons.request import Request
from .chain_handler import ChainHandler

from .customer import CustomerValidator


class CustomerHandler(ChainHandler):
    def handle(self, request: Request):
        validator = CustomerValidator()
        #tomar la decisión de pasar al siguiente eslabón o no
        try:
            validator.validate(request.customer_data)
            # si no levanta una excepción, pasa al siguiente eslabón
            if self._next_handler:
                self._next_handler.handle(request)
        except Exception as e:
            print("error")
            raise e
