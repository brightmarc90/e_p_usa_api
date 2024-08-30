from pydantic import BaseModel

class NameStats_Schema(BaseModel):
    year: int
    fistname: str
    gender: str
    nb_occur: int