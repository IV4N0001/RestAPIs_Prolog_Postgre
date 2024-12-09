from sqlalchemy import Column, Float, ForeignKey, Integer, String
from connection import Base
from sqlalchemy.orm import relationship

class Mascota(Base):
    __tablename__ = "MASCOTAS"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    raza = Column(String, nullable=True)
    edad = Column(String, nullable=True)
    genero = Column(String, nullable=False)
    peso = Column(Float, nullable=True)
    id_dueño = Column(Integer, ForeignKey("DUEÑOS.id"), nullable=False)
    estado = Column(String, nullable=False)

    #dueño = relationship("Dueño", back_populates="mascotas")
    #detalles = relationship("Detalle_Mascota", back_populates="mascota")
    
    
    

