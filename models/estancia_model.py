from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer, func
from connection import Base
from sqlalchemy.orm import relationship

class Estancia(Base):
    __tablename__ = "ESTANCIAS"

    id = Column(Integer, primary_key=True, index=True)
    id_detalle_mascota = Column(Integer, ForeignKey("DETALLES_MASCOTAS.id"), nullable=False)
    id_cuarto = Column(Integer, ForeignKey("CUARTOS.id"), nullable=False)
    inicio_estancia = Column(String, nullable=False)  # Valor predeterminado
    fin_estancia = Column(String, nullable=False)
    importe = Column(Float, nullable=False)
    
    #detalle_mascota = relationship("Detalle_Mascota", back_populates="estancias")
    #cuarto = relationship("Cuarto", back_populates="Estancias")