from pydantic import BaseModel, RootModel
from typing import List
from datetime import date
from typing import Optional

class Violation(BaseModel):
    violation_description: Optional[str] = None
    violation_date: Optional[date] = None
    id:Optional[str] = None

class MVRData(BaseModel):
    id:Optional[str] = None
    name: Optional[str] = None
    license_number: Optional[str] = None
    state: Optional[str] = None
    order_date: Optional[date] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    state_of_driver_record: Optional[str] = None
    driver_address: Optional[str] = None
    driver_city: Optional[str] = None
    driver_state: Optional[str] = None
    driver_zip: Optional[str] = None
    dob: Optional[date] = None
    issued_date: Optional[date] = None
    expiration_date: Optional[date] = None
    license_status: Optional[str] = None
    lic_class: Optional[str] = None
    violations: List[Violation]

# or Pydantic v2
class MVRDriverList(RootModel[List[MVRData]]):
    pass
