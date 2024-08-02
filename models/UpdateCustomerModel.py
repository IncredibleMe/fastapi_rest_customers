from typing import List, Optional
from pydantic import BaseModel


class UpdateCustomerRequest(BaseModel):
    tautotita: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    addresses: Optional[List[dict]]
    phone_numbers: Optional[List[int]]