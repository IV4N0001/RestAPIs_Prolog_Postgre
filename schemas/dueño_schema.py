from pydantic import BaseModel

class DueñoBase(BaseModel):
    nombre: str
    telefono: str
    email: str
    estado: str

class DueñoCreate(DueñoBase):
    pass

class DueñoUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    email: str | None = None
    estado: str | None = None

class DueñoResponse(DueñoBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
