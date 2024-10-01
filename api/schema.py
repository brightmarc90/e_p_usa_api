from pydantic import BaseModel
from typing import List

class BirthSexYear_Schema(BaseModel):
    year: int
    F: int
    M: int

class Proportion_Schema(BaseModel):
    year: int
    firstname: str
    gender: str
    nb_occur: int
    total_by_sex: int
    proportion: float

class YearObject_Schema(BaseModel):
    year: int
    total: int

class FirstnameObject_Schema(BaseModel):
    firstname: str
    total: int

class PivotYearName_Schema(BaseModel):
    firstname: str
    years: List[YearObject_Schema]

class NameStats_Schema(BaseModel):
    year: int
    firstname: str
    gender: str
    nb_occur: int

class UniqueNameCount_Scheme(BaseModel):
    year: int
    unique_firstnames_count: int

class PivotNameYear_Schema(BaseModel):
    year: int
    firstnames: List[FirstnameObject_Schema]