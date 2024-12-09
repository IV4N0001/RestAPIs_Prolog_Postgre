from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import get_db, ejecutar_prolog
from models.hotel_model import Hotel
from schemas.hotel_schema import HotelCreate, HotelUpdate, HotelResponse

router = APIRouter()

@router.post("/crear_hotel", response_model=HotelResponse)
def crear_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    nuevo_hotel = Hotel(nombre=hotel.nombre)
    db.add(nuevo_hotel)
    db.commit()
    db.refresh(nuevo_hotel)
    return nuevo_hotel

@router.get("/get_hoteles")
def get_hoteles():
    try:
        # Llamar a la regla `get_hoteles` en Prolog
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_hoteles")
        
        # Procesar la salida de Prolog
        hoteles = []
        for linea in prolog_output.split("\n"):
            if linea.strip():  # Asegurarse de que la línea no esté vacía
                try:
                    # Suponiendo que la salida es algo como "1, 1er HOTEL"
                    id_hotel, nombre = linea.split(",")
                    hoteles.append({
                        "id": int(id_hotel.strip()),  # Convertir id a entero
                        "nombre": nombre.strip()      # Eliminar espacios adicionales
                    })
                except ValueError:
                    # Si hay un error al procesar la línea, omitirla
                    continue

        return hoteles

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_hotel_by_id/{id}")
def get_hotel_by_id(id: int):
    try:
        # Llamar a Prolog para obtener el hotel con el ID solicitado
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_hotel_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")  # Depuración

        # Procesar la salida de Prolog
        hotel = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:  # Verifica que la línea no esté vacía
                try:
                    # Parsear la línea con formato "1, 1er HOTEL"
                    id_hotel, nombre = linea.split(",", maxsplit=1)
                    hotel = {
                        "id": int(id_hotel.strip()),
                        "nombre": nombre.strip()
                    }
                    break  # Si encontramos el hotel, salimos del bucle
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if hotel:
            return hotel
        else:
            raise HTTPException(status_code=404, detail="Hotel no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/actualizar/{id}", response_model=HotelResponse)
def actualizar_hotel(id: int, hotel_actualizado: HotelUpdate, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    if hotel_actualizado.nombre is not None:
        hotel.nombre = hotel_actualizado.nombre

    db.commit()
    db.refresh(hotel)
    return hotel

@router.delete("/eliminar/{id}", response_model=dict)
def eliminar_hotel(id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    db.delete(hotel)
    db.commit()
    return {"message": "Hotel eliminado correctamente"}