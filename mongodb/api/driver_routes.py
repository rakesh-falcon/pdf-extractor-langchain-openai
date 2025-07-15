from fastapi import APIRouter,HTTPException
from mongodb.schemas.driver_schema import DriverIn, DriverOut
from mongodb.services.driver_service import DriverService
from mongodb.schemas.driver_with_loss_schema import DriverWithLossRuns


router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverOut)
async def create_driver(driver: DriverIn):
    return await DriverService.create_driver(driver)

@router.get("/", response_model=list[DriverOut])
async def get_all_drivers():
    return await DriverService.get_all_drivers()

@router.get("/{driver_id}", response_model=DriverWithLossRuns)
async def get_driver_with_losses(driver_id: str):
    driver = await DriverService.get_driver_with_losses(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver