from pydantic import BaseModel

# 클라이언트에서 서버로 전달하는 데이터의 형식(구조)을 정의
class PersonCreate(BaseModel):
    name: str
    age: int

# 서버에서 클라이언트로 응답하는 데이터의 형식(구조)을 정의
class PersonResponse(PersonCreate):
    id: int

    class Config:
        orm_mode = True  # ORM 모델과 호환 가능하도록 설정