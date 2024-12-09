from pydantic import BaseModel

class CuartoBase(BaseModel):
    id_hotel: int
    numero_cuarto: int
    disponible: bool

class CuartoCreate(CuartoBase):
    pass

class CuartoUpdate(BaseModel):
    numero_cuarto: int | None = None
    disponible: bool | None = None

class CuartoResponse(CuartoBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
