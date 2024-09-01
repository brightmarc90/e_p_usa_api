from api.database import collection
from fastapi import HTTPException, status
import pandas as pd
from typing import Union

def getYearList():
    return collection.distinct("year")

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

async def verify_proportion(start_year: int, end_year: Union[int, None] = None):
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