from pydantic import BaseModel, RootModel
from typing import Optional, Union, List
from datetime import date

class FieldWithConf(BaseModel):
    value: Optional[Union[str, date]] = None
    conf: Optional[float] = None  # You can default to None or 0.0 depending on your logic

class ViolationWithConf(BaseModel):
    violation_description: Optional[FieldWithConf] = FieldWithConf()
    violation_date: Optional[FieldWithConf] = FieldWithConf()

class MVRDataWithConf(BaseModel):
    id: Optional[FieldWithConf] = FieldWithConf()
    name: Optional[FieldWithConf] = FieldWithConf()
    license_number: Optional[FieldWithConf] = FieldWithConf()
    state: Optional[FieldWithConf] = FieldWithConf()
    order_date: Optional[FieldWithConf] = FieldWithConf()
    first_name: Optional[FieldWithConf] = FieldWithConf()
    last_name: Optional[FieldWithConf] = FieldWithConf()
    state_of_driver_record: Optional[FieldWithConf] = FieldWithConf()
    driver_address: Optional[FieldWithConf] = FieldWithConf()
    driver_city: Optional[FieldWithConf] = FieldWithConf()
    driver_state: Optional[FieldWithConf] = FieldWithConf()
    driver_zip: Optional[FieldWithConf] = FieldWithConf()
    dob: Optional[FieldWithConf] = FieldWithConf()
    issued_date: Optional[FieldWithConf] = FieldWithConf()
    expiration_date: Optional[FieldWithConf] = FieldWithConf()
    license_status: Optional[FieldWithConf] = FieldWithConf()
    lic_class: Optional[FieldWithConf] = FieldWithConf()
    violations: Optional[List[ViolationWithConf]] = []

class MVRDriverConfList(RootModel[List[MVRDataWithConf]]):
    pass
