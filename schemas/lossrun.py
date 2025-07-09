from pydantic import BaseModel
from typing import List

class LossRunData(BaseModel):
    insured_name: str
    policy_number: str
    total_paid: str
    losses: List[str]
