from chain_handler import ChainHandler
from payment import PaymentDataValidator
from commons import Request

class PaymentHandler(ChainHandler):
    def handle(self, request:Request):
        validator = PaymentDataValidator()
        #tomar la decisión de pasar al siguiente eslabón o no
        try:
            valid = validator.validate(request.payment_data)
            # si no levanta una excepción, pasa al siguiente eslabón
            if self._next_handler: # solo si el siguiente eslabón existe:
                self._next_handler.handle(request)
        except Exception as e:
            print(e) # payment_validator ya levanta las excepciones.
            raise e
            