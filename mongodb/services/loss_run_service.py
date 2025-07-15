from mongodb.repositories.loss_run_repository import LossRunRepository
from mongodb.schemas.loss_run_schema import LossRunIn

class LossRunService:

    @staticmethod
    async def create_loss_run(loss_run_in: LossRunIn):
        return await LossRunRepository.create(loss_run_in.model_dump())

    @staticmethod
    async def get_all_loss_runs():
        return await LossRunRepository.get_all()