from beanie import Document
from pydantic import Field

class Driver(Document):
    name: str = Field(...)
    license_number: str = Field(...)
    experience_years: int = Field(...)

    class Settings:
        name = "drivers"