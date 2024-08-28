import os
import json

files_location = "../names"

def data_to_json(line:str, year:int):
    lineArray = line.strip().split(",")
    lineObject = {
        "year": year,
        "firstname": lineArray[0],
        "gender": lineArray[1],
        "nb_occur": int(lineArray[2])
    }
    return lineObject

def files_to_list(files_location:str):
    dataList = []
    for file_name in os.listdir(files_location):
        if file_name.endswith(".txt"):     
            file_path = os.path.join(files_location, file_name)
            print(file_path)
            
            with open(file_path, "r") as txt_file:
                for line in txt_file:
                    dataList.append(data_to_json(line, int(file_name[3:7])))
    return dataList

data = files_to_list(files_location)
with open("./output_data/name.json", 'w') as json_file:
    json.dump(data, json_file, indent=4)

