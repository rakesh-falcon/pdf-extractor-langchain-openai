from pydantic import BaseModel, Field
from datetime import date
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "format": "objectid",
            "examples": ["507f1f77bcf86cd799439011"],
        }

class LossRunIn(BaseModel):
    driver_id: PyObjectId = Field(...)
    loss_date: date
    amount: float

class LossRunOut(LossRunIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
    }
