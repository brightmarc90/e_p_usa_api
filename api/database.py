import urllib.parse
from pymongo import MongoClient

# Mot de passe avec des caractères spéciaux doit être encodé
username = "krachenbeatz"
password = "Sonia220364@@@"
encoded_password = urllib.parse.quote_plus(password)

# Construisez l'URI avec le mot de passe encodé
mongo_uri = f"mongodb+srv://{username}:{encoded_password}@epusa.ebpdb.mongodb.net/"

# Initialisez le client MongoDB
client = MongoClient(mongo_uri)

# Accédez à votre base de données et à votre collection
database = client["epusa"]
collection = database["names"]