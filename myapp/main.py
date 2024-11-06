import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .database import engine, get_db

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /static 경로에 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# 루트 경로에서 index.html 파일을 서빙
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)

# 새로운 사용자 추가 (POST 요청)
@app.post("/add_person/", response_model=schemas.PersonResponse)
def add_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    new_person = models.Person(name=person.name, age=person.age)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

# 모든 사용자 조회 (GET 요청)
@app.get("/persons/", response_model=list[schemas.PersonResponse])
def get_persons(db: Session = Depends(get_db)):
    persons = db.query(models.Person).all()
    return persons