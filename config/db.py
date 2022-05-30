from beanie import init_beanie
from schema.item_schema import Item
from schema.user_schema import User
import motor.motor_asyncio


async def initDB():
    """ Initializing MongoDB using motor and init_beanie"""
    client = motor.motor_asyncio.AsyncIOMotorClient\
        ("mongodb+srv://ArunPSIOG:ArunPsiog123@cluster0.xdcfe.mongodb.net/?retryWrites=true&w=majority")#"mongodb://localhost:27017/arun")
    await init_beanie(database=client.hms, document_models=[Item, User])