from mongodb.models.driver import Driver

class DriverRepository:

    @staticmethod
    async def create(data: dict) -> Driver:
        driver = Driver(**data)
        return await driver.insert()

    @staticmethod
    async def get_all():
        return await Driver.find_all().to_list()
    
    @staticmethod
    async def get_by_id(driver_id: str):
        return await Driver.get(driver_id)