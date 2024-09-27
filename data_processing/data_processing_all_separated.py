import os
import json
from pymongo import MongoClient

# Connection MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Assurez-vous que MongoDB tourne sur le port par défaut
db = client["epusa"]  # Remplacez par votre nom de base de données
collection = db["names"]  # Remplacez par le nom de votre collection

files_location = "../names"
output_dir = "./output_data"

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

def process_file(file_path: str, output_file_path: str):
    dataList = []
    with open(file_path, "r") as txt_file:
        for line in txt_file:
            dataList.append(data_to_json(line))
    
    # Enregistrement dans un fichier JSON
    with open(output_file_path, 'w') as json_file:
        json.dump(dataList, json_file, indent=4)
    
    return dataList

def process_files(files_location: str, output_dir: str):
    all_data = []
    
    for file_name in os.listdir(files_location):
        if file_name.lower().endswith(".txt"):
            file_path = os.path.join(files_location, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".json"
            output_file_path = os.path.join(output_dir, output_file_name)
            
            print(f"Processing file: {file_path}")
            
            data = process_file(file_path, output_file_path)
            all_data.extend(data)
    
    return all_data

# Récupération des données
all_data = process_files(files_location, output_dir)

# Insertion dans MongoDB
if all_data:  # S'il y a des données
    collection.insert_many(all_data)
    print(f"Inserted {len(all_data)} documents into MongoDB")
else:
    print("No data found to insert.")
