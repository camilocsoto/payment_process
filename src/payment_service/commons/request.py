"""_summary_
#Este archivo es parte de chain of responsability pattern ☣️
"""
from pydantic import BaseModel
from .payment_data import PaymentData
from .customer import CustomerData

class Request(BaseModel):
    """Encapsula a customer y payment data para validarlos."""
    customer_data: CustomerData
    payment_data: PaymentData