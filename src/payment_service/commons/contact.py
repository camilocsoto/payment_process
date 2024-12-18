from typing import Optional

from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
