from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
Base = declarative_base()


class Festival(Base):
    __tablename__ = "festivals"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(256))
    country = Column("country", String(40))
    city = Column("city", String(40))
    start = Column("start", DateTime)
    end = Column("end", DateTime)

    def __repr__(self):
        return f"Name: {self.name}, Country: {self.country}, City: {self.city}, Start: {self.start}, End: {self.end}"


class Users(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(128))
    email = Column("email", String(128))
    password = Column("password", String(256))

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}, Pass: {self.password}"
