from pydantic import BaseModel
from enum import Enum


class PaymentType(Enum):
    OFFLINE = "offline"
    ONLINE = "online"


class PaymentData(BaseModel):
    amount: int
    source: str
    currency: str = "USD"
    type: PaymentType = PaymentType.ONLINE
