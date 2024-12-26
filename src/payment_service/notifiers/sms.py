from dataclasses import dataclass

from commons import CustomerData

from .notifier import NotifierProtocol


@dataclass
class SMSNotifier(NotifierProtocol):
    #recuerda que si la clase tiene un comportamiento anormal, no cumple con los prinicipios solid y te genera un error al momento de usarlo
    gateway: str

    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        if not phone_number:
            print("No phone number provided")
            return
        print(
            f"SMS sent to {phone_number} via {self.gateway}: Thank you for your payment."
        )
