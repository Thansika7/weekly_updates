from sqlalchemy import Column, Integer, String, Float
from database import Base

class Laptop(Base):

    __tablename__ = "laptops"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String(100))

    ram = Column(Integer)

    inches = Column(Float)

    price = Column(Float)