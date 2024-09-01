from fastapi import FastAPI, status
from api.database import collection
from api import crud
from api.schema import BirthSexYear_Schema
from typing import List, Union

app = FastAPI()

@app.get("/years", response_model=List[int], status_code=status.HTTP_200_OK)
async def getYearList():
    years = await crud.getYearList()
    return years

@app.get("/births", response_model=List[BirthSexYear_Schema], status_code=status.HTTP_200_OK)
async def birthsBySex_Year(start_year: Union[int, None] = None, end_year: Union[int, None] = None):
    births = await crud.birthsBySex_Year(start_year=start_year, end_year=end_year)
    return births

@app.get("/")
async def root():
    cursor = await collection.find().limit(10).to_list(length=None)
    for document in cursor:
        print(document)
    return {"message":"kjfkfjk"}