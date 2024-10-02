from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_uri = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(mongo_uri)
database = client["e_p_usa"]
collection = database["names"]