from sqlalchemy import Column, ForeignKey, Integer, Boolean
from connection import Base
from sqlalchemy.orm import relationship

class Cuarto(Base):
    __tablename__ = "CUARTOS"

    id = Column(Integer, primary_key=True, index=True)
    id_hotel = Column(Integer, ForeignKey("HOTELES.id"), nullable=False)  # Relación
    numero_cuarto = Column(Integer, nullable=False)
    disponible = Column(Boolean, nullable=False)

    #hotel = relationship("Hotel", back_populates="cuartos")
    #estancias = relationship("Estancia", back_populates="cuarto")
