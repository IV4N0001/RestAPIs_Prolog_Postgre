from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Boolean, String, Text
from connection import Base
from sqlalchemy.orm import relationship

class Detalle_Mascota(Base):
    __tablename__ = "DETALLES_MASCOTAS"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("MASCOTAS.id"), nullable=False)
    inicio_desayuno = Column(String, nullable=False)
    fin_desayuno = Column(String, nullable=False)
    inicio_comida = Column(String, nullable=False)
    fin_comida = Column(String, nullable=False)
    agresividad = Column(Boolean, nullable=False)
    temperatura_ideal = Column(Float, nullable=False)
    comentarios = Column(Text, nullable=True)

    #mascota = relationship("Mascota", back_populates="detalles")
    #estancias = relationship("Estancia", back_populates="detalle_mascota")