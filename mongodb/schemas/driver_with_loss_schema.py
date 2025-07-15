from pydantic import BaseModel
from datetime import date

class LossRunOut(BaseModel):
    id: str
    driver_id: str
    loss_date: date
    amount: float

class DriverWithLossRuns(BaseModel):
    id: str
    name: str
    license_number: str
    experience_years: int
    losses: list[LossRunOut]
