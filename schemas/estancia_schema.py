from pydantic import BaseModel

# Esquema base para un estancia (utilizado en Create y Update)
class EstanciaBase(BaseModel):
    id_detalle_mascota: int
    id_cuarto: int
    inicio_estancia: str
    fin_estancia: str
    importe: float

# Esquema para crear un nuevo estancia
class EstanciaCreate(EstanciaBase):
    pass

# Esquema para actualizar un estancia (opcional)
class EstanciaUpdate(BaseModel):
    importe: float | None = None
    
# Esquema para la respuesta que será enviada al cliente
class EstanciaResponse(EstanciaBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
