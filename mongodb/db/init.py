import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from mongodb.models.driver import Driver
from mongodb.models.loss_run import LossRun
from dotenv import load_dotenv

load_dotenv()
# MONGO_URL="mongodb+srv://rakeshfalconsystem:oPG3XxyvIiw54QcM@cluster0.nyl3ud2.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0"
async def init_db():
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        raise ValueError("MONGO_URL not found in environment variables")
    
    client = AsyncIOMotorClient(MONGO_URL)
    db_name = MONGO_URL.split("/")[-1].split("?")[0] or "mydatabase"
    await init_beanie(database=client[db_name], document_models=[Driver, LossRun])
