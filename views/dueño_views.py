from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.dueño_schema import DueñoResponse, DueñoCreate, DueñoUpdate
from models.dueño_model import Dueño
from connection import ejecutar_prolog, get_db

router = APIRouter()

@router.post("/crear_dueño", response_model=DueñoResponse)
def crear_dueño(dueño: DueñoCreate, db: Session = Depends(get_db)):
    nuevo_dueño = Dueño(**dueño.model_dump())
    db.add(nuevo_dueño)
    db.commit()
    db.refresh(nuevo_dueño)
    return nuevo_dueño

@router.get("/get_dueños")
def get_dueños():
    try:
        # Llamar a la regla `get_hoteles` en Prolog
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_dueños")
        
        # Procesar la salida de Prolog
        dueños = []
        for linea in prolog_output.split("\n"):
            if linea.strip():  # Asegurarse de que la línea no esté vacía
                try:
                    # Suponiendo que la salida es algo como "1, 1er HOTEL"
                    id_dueño, nombre, telefono, email, estado = linea.split(",")
                    dueños.append({
                        "id": int(id_dueño.strip()),  # Convertir id a entero
                        "nombre": nombre.strip(),      # Eliminar espacios adicionales
                        "telefono": telefono.strip(),
                        "email": email.strip(),
                        "estado": estado.strip()
                    })
                except ValueError:
                    # Si hay un error al procesar la línea, omitirla
                    continue

        return dueños

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_dueño_by_id/{id}")
def get_dueño_by_id(id: int):
    try:
        # Llamar a Prolog para obtener el hotel con el ID solicitado
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_dueño_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")  # Depuración

        # Procesar la salida de Prolog
        dueño = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:  # Verifica que la línea no esté vacía
                try:
                    # Parsear la línea con formato "1, 1er HOTEL"
                    id_dueño, nombre, telefono, email, estado = linea.split(",", maxsplit=4)
                    dueño = {
                        "id": int(id_dueño.strip()),
                        "nombre": nombre.strip(),
                        "telefono": telefono.strip(),
                        "email": email.strip(),
                        "estado": estado.strip()
                    }
                    break  # Si encontramos el hotel, salimos del bucle
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if dueño:
            return dueño
        else:
            raise HTTPException(status_code=404, detail="Dueño no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/actualizar/{id}", response_model=DueñoResponse)
def actualizar_dueño(id: int, dueño_actualizado: DueñoUpdate, db: Session = Depends(get_db)):
    dueño = db.query(Dueño).filter(Dueño.id == id).first()
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    if dueño_actualizado.nombre is not None:
        dueño.nombre = dueño_actualizado.nombre
    if dueño_actualizado.telefono is not None:
        dueño.telefono = dueño_actualizado.telefono
    if dueño_actualizado.email is not None:
        dueño.email = dueño_actualizado.email
    if dueño_actualizado.estado is not None:
        dueño.estado = dueño_actualizado.estado

    db.commit()
    db.refresh(dueño)
    return dueño

@router.delete("/eliminar/{id}", response_model=dict)
def eliminar_dueño(id: int, db: Session = Depends(get_db)):
    dueño = db.query(Dueño).filter(Dueño.id == id).first()
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    db.delete(Dueño)
    db.commit()
    return {"message": "Dueño eliminado correctamente"}

