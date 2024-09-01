from pydantic import BaseModel

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

class NameStats_Schema(BaseModel):
    year: int
    firstname: str
    gender: str
    nb_occur: int
