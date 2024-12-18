from typing import Protocol

from commons import CustomerData


class NotifierProtocol(Protocol):
    """Protocol for sending notifications.

    This protocol defines the interface for notifiers. Implementations
    should provide a method `send_confirmation` that sends a confirmation
    to the customer.
    """

    def send_confirmation(self, customer_data: CustomerData): ...
