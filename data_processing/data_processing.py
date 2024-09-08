import os
import json
from pymongo import MongoClient

# Connection MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Assurez-vous que MongoDB tourne sur le port par défaut
db = client["e_p_usa"]  # Remplacez par votre nom de base de données
collection = db["names"]  # Remplacez par le nom de votre collection

files_location = "../names"


def data_to_json(line: str):
    lineArray = line.strip().split(",")
    lineObject = {
        "state": lineArray[0],       # État (AK)
        "gender": lineArray[1],      # Genre (F)
        "year": int(lineArray[2]),   # Année (1927)
        "firstname": lineArray[3],   # Prénom (Lillian)
        "nb_occur": int(lineArray[4])  # Nombre d'occurrences (5)
    }
    return lineObject


def files_to_list(files_location: str):
    dataList = []
    for file_name in os.listdir(files_location):
        if file_name.endswith(".txt") or file_name.endswith(".TXT"):
            file_path = os.path.join(files_location, file_name)
            print(f"Processing file: {file_path}")
            
            with open(file_path, "r") as txt_file:
                for line in txt_file:
                    dataList.append(data_to_json(line))  # Assurez-vous que l'année est aux bonnes positions

    return dataList


# Récupération des données
data = files_to_list(files_location)

# Vérification et création du dossier output_data
output_dir = "./output_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Enregistrement dans un fichier JSON
with open(os.path.join(output_dir, "name.json"), 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Insertion dans MongoDB
if data:  # S'il y a des données
    collection.insert_many(data)
    print(f"Inserted {len(data)} documents into MongoDB")
else:
    print("No data found to insert.")
