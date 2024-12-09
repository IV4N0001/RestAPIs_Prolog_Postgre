from pydantic import BaseModel

class EstanciaBase(BaseModel):
    id_detalle_mascota: int
    id_cuarto: int
    inicio_estancia: str
    fin_estancia: str
    importe: float

class EstanciaCreate(EstanciaBase):
    pass

class EstanciaUpdate(BaseModel):
    importe: float | None = None
    
class EstanciaResponse(EstanciaBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
