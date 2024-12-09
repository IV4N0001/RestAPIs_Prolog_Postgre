from pydantic import BaseModel

class HotelBase(BaseModel):
    nombre: str

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    nombre: str | None = None

class HotelResponse(HotelBase):
    id: int

    class Config:
        orm_mode = True
