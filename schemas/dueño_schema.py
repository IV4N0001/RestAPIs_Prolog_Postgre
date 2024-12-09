from pydantic import BaseModel

# Esquema base para un Dueño (utilizado en Create y Update)
class DueñoBase(BaseModel):
    nombre: str
    telefono: str
    email: str
    estado: str

# Esquema para crear un nuevo dueño
class DueñoCreate(DueñoBase):
    pass

# Esquema para actualizar un dueño (opcional)
class DueñoUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    email: str | None = None
    estado: str | None = None

# Esquema para la respuesta que será enviada al cliente
class DueñoResponse(DueñoBase):
    id: int

    class Config:
        orm_mode = True  # Permite que se pueda convertir el objeto SQLAlchemy a dict
