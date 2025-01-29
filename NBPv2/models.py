from sqlalchemy import Column, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currencies'

    # Zdefiniowanie kolumn tabeli
    code = Column(String, primary_key=True)
    name = Column(String)
    rate = Column(Float)
    date = Column(Date, primary_key=True)