from api.database import collection
from fastapi import HTTPException, status
import pandas as pd
from typing import Union, List

def getYearList():
    return collection.distinct("year")

async def getFirtsname(param: str):
    match_conditions = {}
    pipeline = []
    if param:
        match_conditions["firstname"] = {"$regex": param, "$options": "i"}
    if match_conditions:
        pipeline.append({"$match": match_conditions})
    
    pipeline.append({"$group": {"_id": "$firstname"}})
    pipeline.append({"$project": {"_id": 0, "firstname": "$_id"}})
    firstnames = await collection.aggregate(pipeline).to_list(length=None)
    return firstnames

async def birthsBySex_Year(start_year: Union[int, None] = None, end_year: Union[int, None] = None):
    match_conditions = {}
    pipeline = []
    if start_year and end_year:
        match_conditions["year"] = {"$gte": start_year, "$lte": end_year}
    elif start_year:
        match_conditions["year"] = start_year

    if match_conditions:
        pipeline.append({"$match": match_conditions})
    
    pipeline.append({
            "$group": {
                "_id": {"year":"$year", "gender":"$gender"},
                "total": {
                    "$sum": "$nb_occur"
                }
            }
        })
    births = await collection.aggregate(pipeline).to_list(length=None)
    if not births:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun résultat")
    data = [{
            "year": birth["_id"]["year"],
            "gender": birth["_id"]["gender"],
            "nb_births": birth["total"]} for birth in births]
    df = pd.DataFrame(data)
    print(df.head())
    pivot = df.pivot_table(values="nb_births", index="year", columns="gender", aggfunc="sum")
    pivot = pivot.reset_index().to_dict(orient="records")
    return pivot

async def verify_proportion(start_year: int, end_year: Union[int, None] = None): # logique à revoir
    match_conditions = {}
    pipeline = []
    if start_year and end_year:
        match_conditions["year"] = {"$gte": start_year, "$lte": end_year}
    elif start_year:
        match_conditions["year"] = start_year

    if match_conditions:
        pipeline.append({"$match": match_conditions})

    pipeline.append({"$project": {"_id": 0}})

    births = await collection.aggregate(pipeline).to_list(length=None)
    if not births:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun résultat")
    df = pd.DataFrame(births)
    df["total_by_sex"] = df.groupby(["year", "gender"])["nb_occur"].transform("sum")
    df["proportion"] = df["nb_occur"] / df["total_by_sex"]
    return df.to_dict(orient="records")

async def pivotFirstname_year(params: List[str], start_year: int, end_year: Union[int, None] = None):
    match_conditions = {}
    pipeline = []
    if start_year and end_year:
        match_conditions["year"] = {"$gte": start_year, "$lte": end_year}
    elif start_year:
        match_conditions["year"] = start_year

    if not params:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun résultat")
    match_conditions["firstname"] = {"$in": params}
    pipeline.append({"$match": match_conditions})
    pipeline.append({"$group": {"_id": ["$year","$firstname"], "total": {"$sum": "$nb_occur"}}})
    births = await collection.aggregate(pipeline).to_list(length=None)
    #print(births)
    """ data = [{
            "year": birth["_id"][0],
            "firstname": birth["_id"][1],
            "total": birth["total"]} for birth in births] """
    """  data = [{"firstname": birth["_id"][1],
             "years":[{"year": sBirth["_id"][0], "total": sBirth["total"]} for sBirth in births 
                      if (birth["_id"][1] == sBirth["_id"][1])]} for birth in births] """
    data = []
    for birth in births:
        birthObject = {}       
        birthObject["firstname"] = birth["_id"][1]
        birthObject["years"] = []
        for birth2 in births:
            if birth["_id"][1] == birth2["_id"][1]:
                birthObject["years"].append({"year": birth2["_id"][0], "total": birth2["total"]})
        if birthObject["firstname"] not in [ elmt["firstname"] for elmt in data]:
            data.append(birthObject)
    return data