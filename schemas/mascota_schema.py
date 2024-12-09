from pydantic import BaseModel

# Esquema base para un Dueño (utilizado en Create y Update)
class MascotaBase(BaseModel):
    nombre: str
    raza: str
    edad: str
    genero: str
    peso: float
    id_dueño: int
    estado: str

# Esquema para crear un nuevo dueño
class MascotaCreate(MascotaBase):
    pass

# Esquema para actualizar un dueño (opcional)
class MascotaUpdate(BaseModel):
    nombre: str | None = None
    raza: str | None = None
    edad: str | None = None
    genero: str | None = None
    peso: float | None = None
    estado: str | None = None

# Esquema para la respuesta que será enviada al cliente
class MascotaResponse(MascotaBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
