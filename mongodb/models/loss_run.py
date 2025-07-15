# app/models/loss_run.py
from beanie import Document
from pydantic import Field
from datetime import date
from bson import ObjectId

class LossRun(Document):
    driver_id: ObjectId = Field(...)
    loss_date: date = Field(...)
    amount: float = Field(...)

    class Settings:
        name = "lossruns"

    class Config:
        arbitrary_types_allowed = True
