from fastapi import FastAPI, status
from api.database import collection
from api import crud
from api.schema import *
from typing import List, Union

app = FastAPI()

@app.get("/years", response_model=List[int], status_code=status.HTTP_200_OK)
async def getYearList():
    years = await crud.getYearList()
    return years

@app.get("/firstnames", response_model=List[dict], status_code=status.HTTP_200_OK)
async def getFirstnameList(param: str):
    firstnames = await crud.getFirtsname(param=param)
    return firstnames

@app.get("/births", response_model=List[BirthSexYear_Schema], status_code=status.HTTP_200_OK)
async def birthsBySex_Year(start_year: Union[int, None] = None, end_year: Union[int, None] = None):
    births = await crud.birthsBySex_Year(start_year=start_year, end_year=end_year)
    return births

@app.get("/group-proportions", response_model=List[Proportion_Schema], status_code=status.HTTP_200_OK)
async def verify_proportion(start_year: int = 2018, end_year: Union[int, None] = None):
    proportions = await crud.verify_proportion(start_year=start_year, end_year=end_year)
    return proportions

@app.post("/year-name-pivot", response_model=List[PivotYearName_Schema], status_code=status.HTTP_200_OK)
async def pivotFirstname_year(params: List[str], start_year: int = 2018, end_year: Union[int, None] = None):
    pivot_data = await crud.firstname_trends(params=params, start_year=start_year, end_year=end_year)
    return pivot_data

@app.post("/name-trends", response_model=List[PivotYearName_Schema],status_code=status.HTTP_200_OK)
async def firstname_trends(params: List[str], start_year: int = 2018, end_year: Union[int, None] = None):
    trends = await crud.firstname_trends(params=params, start_year=start_year, end_year=end_year)
    return trends

@app.get("/")
async def root():
    cursor = await collection.find().limit(10).to_list(length=None)
    for document in cursor:
        print(document)
    return {"message":"kjfkfjk"}