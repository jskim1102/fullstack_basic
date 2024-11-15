from pydantic import BaseModel

class PersonCreate(BaseModel):
    name: str
    passwd: int

class PersonResponse(PersonCreate):
    id: int

    class Config:
        orm_mode = True  # ORM 모델과 호환 가능하도록 설정