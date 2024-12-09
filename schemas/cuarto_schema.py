from pydantic import BaseModel

# Esquema base para un Dueño (utilizado en Create y Update)
class CuartoBase(BaseModel):
    id_hotel: int
    numero_cuarto: int
    disponible: bool

# Esquema para crear un nuevo dueño
class CuartoCreate(CuartoBase):
    pass

# Esquema para actualizar un dueño (opcional)
class CuartoUpdate(BaseModel):
    numero_cuarto: int | None = None
    disponible: bool | None = None

# Esquema para la respuesta que será enviada al cliente
class CuartoResponse(CuartoBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
