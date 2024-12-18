from pydantic import BaseModel

from .customer import CustomerData
from .payment_data import PaymentData


class Request(BaseModel):
    customer_data: CustomerData
    payment_data: PaymentData
