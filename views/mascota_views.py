from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.mascota_schema import MascotaResponse, MascotaCreate, MascotaUpdate
from models.mascota_model import Mascota

from connection import ejecutar_prolog, get_db

router = APIRouter()

@router.post("/crear_mascota", response_model=MascotaResponse)
def crear_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    nuevo_mascota = Mascota(**mascota.model_dump())
    db.add(nuevo_mascota)
    db.commit()
    db.refresh(nuevo_mascota)
    return nuevo_mascota

@router.get("/get_mascotas")
def get_mascotas():
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_mascotas")

        mascotas = []
        for linea in prolog_output.split("\n"):
            if linea.strip():
                try:
                    id_mascota, nombre, raza, edad, genero, peso, id_dueño, estado = linea.split(",")
                    mascotas.append({
                        "id": int(id_mascota.strip()),
                        "nombre": nombre.strip(),
                        "raza": raza.strip(),
                        "edad": edad.strip(),
                        "genero": genero.strip(),
                        "peso": float(peso.strip()),
                        "id_dueño": int(id_dueño.strip()),
                        "estado": estado.strip()
                    })
                except ValueError:
                    # Si hay un error al procesar la línea, omitirla
                    continue

        return mascotas
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_mascota_by_id/{id}")
def get_mascota_by_id(id: int):
    try:
        # Llamar a Prolog para obtener el mascota con el ID solicitado
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_mascota_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")  # Depuración

        # Procesar la salida de Prolog
        mascota = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:  # Verifica que la línea no esté vacía
                try:
                    # Parsear la línea con formato "1, 1er HOTEL"
                    id_mascota, nombre, raza, edad, genero, peso, id_dueño, estado = linea.split(",")

                    mascota = {
                        "id": int(id_mascota.strip()),
                        "nombre": nombre.strip(),
                        "raza": raza.strip(),
                        "edad": edad.strip(),
                        "genero": genero.strip(),
                        "peso": float(peso.strip()),
                        "id_dueño": int(id_dueño.strip()),
                        "estado": estado.strip()
                    }
                    break  # Detener el bucle después de encontrar el primer resultado
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if mascota:
            return mascota
        else:
            raise HTTPException(status_code=404, detail="mascota no encontrada")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/actualizar/{id}", response_model=MascotaResponse)
def actualizar_mascota(id: int, mascota_actualizado: MascotaUpdate, db: Session = Depends(get_db)):
    mascota = db.query(mascota).filter(mascota.id == id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="mascota no encontrada")
    
    if mascota_actualizado.nombre is not None:
        mascota.nombre = mascota_actualizado.nombre
    if mascota_actualizado.raza is not None:
        mascota.raza = mascota_actualizado.raza
    if mascota_actualizado.edad is not None:
        mascota.edad = mascota_actualizado.edad
    if mascota_actualizado.genero is not None:
        mascota.genero = mascota_actualizado.genero
    if mascota_actualizado.peso is not None:
        mascota.peso = mascota_actualizado.peso
    if mascota_actualizado.estado is not None:
        mascota.estado = mascota_actualizado.estado

@router.delete("/eliminar/{id}", response_model=dict)
def eliminar_mascota(id: int, db: Session = Depends(get_db)):
    mascota = db.query(mascota).filter(mascota.id == id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="mascota no encontrado")
    
    db.delete(mascota)
    db.commit()
    return {"message": "mascota eliminado correctamente"}