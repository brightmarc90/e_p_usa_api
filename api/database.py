# from motor.motor_asyncio import AsyncIOMotorClient
# import os
# import json
from pymongo import MongoClient

# mongo_uri = os.getenv("MONGO_URI")
# client = AsyncIOMotorClient(mongo_uri)
# database = client["e_p_usa"]
# collection = database["names"]


# Connection MongoDB
client = MongoClient("mongodb+srv://krachenbeatz:Sonia220364@@@epusa.ebpdb.mongodb.net/")  # Assurez-vous que MongoDB tourne sur le port par défaut
db = client["epusa"]  # Remplacez par votre nom de base de données
collection = db["names"]  # Remplacez par le nom de votre collection