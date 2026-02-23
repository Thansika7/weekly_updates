from pydantic import BaseModel

class LaptopResponse(BaseModel):

    id: int

    company: str

    ram: int

    inches: float

    price: float

    class Config:

        from_attributes = True