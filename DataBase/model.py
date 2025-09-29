from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
Base = declarative_base()


class Festival(Base):
    __tablename__ = "festival"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(256))
    country = Column("country", String(40))
    city = Column("city", String(40))
    start = Column("start", DateTime)
    end = Column("end", DateTime)
    author = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"Name: {self.name}, Country: {self.country}, City: {self.city}, Start: {self.start}, End: {self.end}"


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(20))
    email = Column("email", String(128))
    password = Column("password", String(128))
    image = Column("img", String(20), default='Image/default.jpg')

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}"
