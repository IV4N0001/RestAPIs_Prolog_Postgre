from sqlalchemy import Column, Integer, String
from connection import Base

class Dueño(Base):
    __tablename__ = "DUEÑOS"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, nullable=False)
    estado = Column(String, nullable=False)

    #mascotas = relationship("Mascota", back_populates="dueño")