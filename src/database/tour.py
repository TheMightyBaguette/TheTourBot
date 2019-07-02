from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tour(Base):
    __tablename__ = "tour"
    userid = Column(String, primary_key=True)
    played = Column(Boolean, default=False)
    action = Column(String)
