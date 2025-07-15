from mongodb.repositories.driver_repository import DriverRepository
from mongodb.schemas.driver_schema import DriverIn
from mongodb.repositories.loss_run_repository import LossRunRepository
from mongodb.schemas.driver_with_loss_schema import DriverWithLossRuns
from bson import ObjectId
class DriverService:

    @staticmethod
    async def create_driver(driver_in: DriverIn):
        return await DriverRepository.create(driver_in.model_dump())

    @staticmethod
    async def get_all_drivers():
        return await DriverRepository.get_all()
    
    @staticmethod
    async def get_driver_with_losses(driver_id: str):
        driver = await DriverRepository.get_by_id(driver_id)
        if not driver:
            return None

        loss_runs = await LossRunRepository.get_by_driver_id(ObjectId(driver_id))

        return DriverWithLossRuns(
            id=str(driver.id),
            name=driver.name,
            license_number=driver.license_number,
            experience_years=driver.experience_years,
            losses=[
                {
                    "id": str(loss.id),
                    "driver_id": str(loss.driver_id),
                    "loss_date": loss.loss_date,
                    "amount": loss.amount
                }
                for loss in loss_runs
            ]
        )