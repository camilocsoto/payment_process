from typing import Protocol

from commons import CustomerData


class NotifierProtocol(Protocol):
    """Protocol/Interface for sending notifications.

    This protocol defines the interface for notifiers. Implementations
    should provide a method `send_confirmation` that sends a confirmation
    to the customer.
    
    This protocol is implemented by email y sms
    """

    def send_confirmation(self, customer_data: CustomerData): ...
