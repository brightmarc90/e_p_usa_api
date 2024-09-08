# from motor.motor_asyncio import AsyncIOMotorClient
# import os
# import json
from pymongo import MongoClient

# mongo_uri = os.getenv("MONGO_URI")
# client = AsyncIOMotorClient(mongo_uri)
# database = client["e_p_usa"]
# collection = database["names"]


# Connection MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Assurez-vous que MongoDB tourne sur le port par défaut
db = client["e_p_usa"]  # Remplacez par votre nom de base de données
collection = db["names"]  # Remplacez par le nom de votre collection