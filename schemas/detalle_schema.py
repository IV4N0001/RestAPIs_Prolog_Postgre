from pydantic import BaseModel

class DetalleBase(BaseModel):
    id_mascota: int
    inicio_desayuno: str
    fin_desayuno: str
    inicio_comida: str
    fin_comida: str
    agresividad: bool
    temperatura_ideal: float
    comentarios: str

class DetalleCreate(DetalleBase):
    pass

class DetalleUpdate(BaseModel):
    inicio_desayuno: str | None = None
    fin_desayuno: str | None = None
    inicio_comida: str | None = None
    fin_comida: str | None = None
    agresividad: bool | None = None
    temperatura_ideal: float | None = None
    comentarios: str | None = None

class DetalleResponse(DetalleBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict