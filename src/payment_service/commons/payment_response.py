from typing import Optional

from pydantic import BaseModel


class PaymentResponse(BaseModel):
    status: str
    amount: int
    transaction_id: Optional[str] = None
    message: Optional[str] = None
