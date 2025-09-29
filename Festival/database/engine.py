from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Festival.database.model import Base
engine_obj = create_engine(
    "sqlite:///base.db", future=True, echo=True)
Session = sessionmaker(bind=engine_obj)

def create():
    Base.metadata.create_all(bind=engine_obj)

def drop():
    Base.metadata.drop_all(bind=engine_obj)
