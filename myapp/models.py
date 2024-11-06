from sqlalchemy import Column, Integer, String
from .database import Base

class Person(Base):
    __tablename__ = "collection_jinsoo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)