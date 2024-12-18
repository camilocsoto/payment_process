from pydantic import BaseModel

from typing import Optional
from .contact import ContactInfo


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: Optional[str] = None
