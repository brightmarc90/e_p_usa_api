from pydantic import BaseModel

class BirthSexYear_Schema(BaseModel):
    year: int
    F: int
    M: int
    
class NameStats_Schema(BaseModel):
    year: int
    fistname: str
    gender: str
    nb_occur: int
