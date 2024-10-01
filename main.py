from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from api.database import collection
from api import crud
from api.schema import *
from typing import List, Union

app = FastAPI()

origins = [
    "http://localhost", # Autorise les requêtes depuis localhost
    "http://localhost:3000", # front-end React exécuté sur le port 3000
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/name-diversity", response_model=List[UniqueNameCount_Scheme], status_code=status.HTTP_200_OK)
async def firstnameDiversity_year(start_year: int = 2018, end_year: Union[int, None] = None):
    results = await crud.year_count_unique_firstname(start_year=start_year, end_year=end_year)
    return results

@app.post("/name-diversity-params", response_model=List[PivotNameYear_Schema],status_code=status.HTTP_200_OK)
async def firstnameDiversity_year_params(params: List[str], start_year: int = 2018, end_year: Union[int, None] = None):
    results = await crud.year_firstname_trends(params=params, start_year=start_year, end_year=end_year)
    return results

@app.post("/decade-trends", status_code=status.HTTP_200_OK)
async def decade_trends(params: List[str], start_year: int = 1880, end_year: Union[int, None] = None):
    results = await crud.births_by_decade(params=params, start_year=start_year, end_year=end_year)
    return results

@app.get("/name-length-trends", status_code=status.HTTP_200_OK)
async def name_length_trends(start_year: int = 1880, end_year: Union[int, None] = None):
    results = await crud.births_by_name_length(start_year=start_year, end_year=end_year)
    return results

@app.get("/")
async def root():
    cursor = await collection.find().limit(10).to_list(length=None)
    for document in cursor:
        print(document)
    return {"message":"kjfkfjk"}