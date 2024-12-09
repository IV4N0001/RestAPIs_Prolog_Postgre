from sqlalchemy import Column, Integer, String
from connection import Base
from sqlalchemy.orm import relationship

class Hotel(Base):
    __tablename__ = "HOTELES"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    #cuartos = relationship("Cuarto", back_populates="hotel")
