from pydantic import BaseModel

class MascotaBase(BaseModel):
    nombre: str
    raza: str
    edad: str
    genero: str
    peso: float
    id_dueño: int
    estado: str

class MascotaCreate(MascotaBase):
    pass

class MascotaUpdate(BaseModel):
    nombre: str | None = None
    raza: str | None = None
    edad: str | None = None
    genero: str | None = None
    peso: float | None = None
    estado: str | None = None

class MascotaResponse(MascotaBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
