from mongodb.models.loss_run import LossRun
from bson import ObjectId
class LossRunRepository:

    @staticmethod
    async def create(data: dict) -> LossRun:
        loss_run = LossRun(**data)
        return await loss_run.insert()

    @staticmethod
    async def get_all():
        return await LossRun.find_all().to_list()
    
    @staticmethod
    async def get_by_driver_id(driver_id: ObjectId):
        return await LossRun.find(LossRun.driver_id == driver_id).to_list()
        