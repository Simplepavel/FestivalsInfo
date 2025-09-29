from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from DataBase.model import Base
engine_obj = create_engine("sqlite:///DataBase/base.db", future=True, echo = True)
Sessesion_obj = sessionmaker(bind=engine_obj)


def create():
    Base.metadata.create_all(bind = engine_obj)

def drop():
    Base.metadata.drop_all(bind = engine_obj)