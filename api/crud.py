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

""" async def pivotFirstname_year(params: List[str], start_year: int, end_year: Union[int, None] = None):
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
    pipeline.append({"$project": {"_id": 0}})
    births = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(births)
    grouped_df = df.groupby(["firstname", "year"]).agg(total=("nb_occur", "sum")).reset_index()
    data = grouped_df.groupby("firstname").apply(
        lambda x: {
        "firstname": x.iloc[0]["firstname"],
        "years": x[['year', 'total']].to_dict(orient='records')
    }
    ).to_list()
    return data """

async def firstname_trends(params: List[str], start_year: int, end_year: Union[int, None] = None):
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
    pipeline.append({"$project": {"_id": 0}})
    births = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(births)
    grouped_df = df.groupby(["firstname", "year"]).agg(total=("nb_occur", "sum")).reset_index()
    data = grouped_df.groupby('firstname').apply(
    lambda x: {
        "firstname": x.iloc[0]["firstname"],
        "years": x[['year', 'total']].to_dict(orient='records')
    }
    ).tolist()
    return data

# récupère une liste avec pour chaque année le nombre de prénoms uniques
async def year_count_unique_firstname(start_year: int, end_year: Union[int, None] = None):
    match_conditions = {}
    pipeline = []
    if start_year and end_year:
        match_conditions["year"] = {"$gte": start_year, "$lte": end_year}
    elif start_year:
        match_conditions["year"] = start_year

    pipeline.append({"$match": match_conditions})
    pipeline.append({
        "$group": {
            "_id": {
                "year": "$year"
            },
            "unique_firstnames": {
                "$addToSet": "$firstname"
            }
        }
    })
    pipeline.append({
        "$project": {
            "year": "$_id.year",
            "unique_firstnames_count": {
                "$size": "$unique_firstnames"
            },
            "_id": 0
        }
    })
    pipeline.append({
        "$sort": {
            "year": 1
        }
    })
    results = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(results)
    return df.to_dict(orient='records')

# récupère une liste avec pour chaque année le nombre d'occurences des prénoms selectionnés
async def year_firstname_trends(params: List[str], start_year: int, end_year: Union[int, None] = None):
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
    pipeline.append({"$project": {"_id": 0}})
    births = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(births)
    grouped_df = df.groupby(["year", "firstname"]).agg(total=("nb_occur", "sum")).reset_index()
    data = grouped_df.groupby('year').apply(
    lambda x: {
        "year": x.iloc[0]["year"],
        "firstnames": x[['firstname', 'total']].to_dict(orient='records')
    }
    ).tolist()
    return data

# récupère le nombre de naissance par année et par prénom et calcule les naissances par décade
async def births_by_decade(params: List[str], start_year: int, end_year: Union[int, None] = None):
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
    pipeline.append({
        "$group": {
        "_id": {"year": "$year", "firstname": "$firstname"},
        "nb_occur": {
            "$sum": "$nb_occur"
        }
        }
    })
    pipeline.append({
        "$project": {
        "year": "$_id.year",
        "firstname": "$_id.firstname",
        "_id": 0,
        "nb_occur": 1
        }
    })
    pipeline.append({
        "$sort": {
        "year": 1,
        "nb_occur": -1
        }
    })
    births = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(births)
    df['decade'] = (df['year'] // 10) * 10
    trend_by_decade = df.groupby(['decade', 'firstname'])['nb_occur'].sum().reset_index()
    data = trend_by_decade.groupby('decade').apply(
    lambda x: {
        "decade": int(x.iloc[0]["decade"]),
        "firstnames": x[['firstname', 'nb_occur']].to_dict(orient='records')
    }
    ).tolist()
    return data

# récupère les naissance par année et par prénom et regroupe sur la longeur des prénoms
async def births_by_name_length(start_year: int, end_year: Union[int, None] = None):
    match_conditions = {}
    pipeline = []
    if start_year and end_year:
        match_conditions["year"] = {"$gte": start_year, "$lte": end_year}
    elif start_year:
        match_conditions["year"] = start_year

    pipeline.append({"$match": match_conditions})
    pipeline.append({
        "$group": {
        "_id": {"year": "$year", "firstname": "$firstname"},
        "nb_occur": {
            "$sum": "$nb_occur"
        }
        }
    })
    pipeline.append({
        "$project": {
        "year": "$_id.year",
        "firstname": "$_id.firstname",
        "_id": 0,
        "nb_occur": 1
        }
    })
    pipeline.append({
        "$sort": {
        "year": 1,
        "nb_occur": -1
        }
    })
    births = await collection.aggregate(pipeline).to_list(length=None)
    df = pd.DataFrame(births)
    df['length'] = df['firstname'].apply(len)
    trend_by_length = df.groupby(['year', 'length'])['nb_occur'].sum().reset_index()
    data = trend_by_length.groupby('year').apply(
    lambda x: {
        "year": int(x.iloc[0]["year"]),
        "lengths": x[['length', 'nb_occur']].to_dict(orient='records')
    }
    ).tolist()
    return data
