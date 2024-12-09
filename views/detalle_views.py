from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.detalle_schema import DetalleResponse, DetalleCreate, DetalleUpdate
from models.detalle_model import Detalle_Mascota
from connection import ejecutar_prolog, get_db
from datetime import datetime

router = APIRouter()

# Crear un nuevo detalle
@router.post("/crear_detalle", response_model=DetalleResponse)
def crear_detalle(detalle: DetalleCreate, db: Session = Depends(get_db)):
    nuevo_detalle = Detalle_Mascota(**detalle.model_dump())
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    return nuevo_detalle

# Obtener todos los detalles
@router.get("/get_detalles")
def get_detalles():
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_detalles")

        detalles = []
        for linea in prolog_output.split("\n"):
            if linea.strip():
                try:
                    (id_detalle, id_mascota, inicio_desayuno, fin_desayuno, inicio_comida, 
                     fin_comida, agresividad, temperatura_ideal, comentarios) = linea.split(",")

                    detalles.append({
                        "id": int(id_detalle.strip()),
                        "id_mascota": int(id_mascota.strip()),
                        "inicio_desayuno": inicio_desayuno.strip(),
                        "fin_desayuno": fin_desayuno.strip(),
                        "inicio_comida": inicio_comida.strip(),
                        "fin_comida": fin_comida.strip(),
                        "agresividad": agresividad.strip().lower() == "true",
                        "temperatura_ideal": float(temperatura_ideal.strip()),
                        "comentarios": comentarios.strip()
                    })
                except ValueError:
                    continue

        return detalles
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un detalle por ID
@router.get("/get_detalle_by_id/{id}")
def get_detalle_by_id(id: int):
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_detalle_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")

        detalle = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:
                try:
                    id_detalle, id_mascota, inicio_desayuno, fin_desayuno, inicio_comida, fin_comida, agresividad_str, temperatura_ideal, comentarios = linea.split(",", maxsplit=8)

                    agresividad = True if agresividad_str.strip().lower() == "true" else False

                    detalle = {
                        "id": int(id_detalle.strip()),
                        "id_mascota": int(id_mascota.strip()),
                        "inicio_desayuno": inicio_desayuno.strip(),
                        "fin_desayuno": fin_desayuno.strip(),
                        "inicio_comida": inicio_comida.strip(),
                        "fin_comida": fin_comida.strip(),
                        "agresividad": agresividad,
                        "temperatura_ideal": float(temperatura_ideal.strip()),
                        "comentarios": comentarios.strip()
                    }
                    break
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if detalle:
            return detalle
        else:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un detalle
@router.patch("/actualizar/{id}", response_model=DetalleResponse)
def actualizar_detalle(id: int, detalle_actualizado: DetalleUpdate, db: Session = Depends(get_db)):
    detalle = db.query(Detalle_Mascota).filter(Detalle_Mascota.id == id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    if detalle_actualizado.inicio_desayuno is not None:
        detalle.inicio_desayuno = detalle_actualizado.inicio_desayuno
    if detalle_actualizado.fin_desayuno is not None:
        detalle.fin_desayuno = detalle_actualizado.fin_desayuno
    if detalle_actualizado.inicio_comida is not None:
        detalle.inicio_comida = detalle_actualizado.inicio_comida
    if detalle_actualizado.fin_comida is not None:
        detalle.fin_comida = detalle_actualizado.fin_comida
    if detalle_actualizado.agresividad is not None:
        detalle.agresividad = detalle_actualizado.agresividad
    if detalle_actualizado.temperatura_ideal is not None:
        detalle.temperatura_ideal = detalle_actualizado.temperatura_ideal
    if detalle_actualizado.comentarios is not None:
        detalle.comentarios = detalle_actualizado.comentarios

    db.commit()
    db.refresh(detalle)
    return detalle

# Eliminar un detalle
@router.delete("/eliminar/{id}", response_model=dict)
def eliminar_detalle(id: int, db: Session = Depends(get_db)):
    detalle = db.query(Detalle_Mascota).filter(Detalle_Mascota.id == id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    db.delete(detalle)
    db.commit()
    return {"message": "Detalle eliminado correctamente"}

@router.get("/es_hora_de_alimentar/{id}")
def es_hora_de_alimentar(id: int) -> bool:
    """
    Determina si es hora de alimentar a la mascota según la regla Prolog `es_hora_de_alimentar`.
    """
    try:
        # Obtener la hora actual en formato "HH:MM"
        hora_actual = datetime.now().strftime("%H:%M")

        # Construir la consulta Prolog con el ID de la mascota y la hora actual
        prolog_query = f"es_hora_de_alimentar({id}, '{hora_actual}')"

        # Ejecutar la consulta en Prolog
        prolog_output = ejecutar_prolog("rules_prolog.pl", prolog_query)

        # Verificar si la salida de Prolog es 'false'
        if prolog_output == "false":
            return False
        elif prolog_output == "true":
            return True
        else:
            raise HTTPException(status_code=500, detail="Respuesta inesperada de Prolog")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/regular_temperatura/{temperatura_actual}/{id}")
def regular_temperatura(temperatura_actual: float, id: int) -> bool:
    """
    Verifica si la temperatura actual está por encima o igual a la temperatura óptima de la mascota.
    """
    try:
        # Construir la consulta Prolog
        prolog_query = f"regular_temperatura({temperatura_actual}, {id})."

        # Imprimir la consulta Prolog para depuración
        print(f"Consulta Prolog: {prolog_query}")

        # Ejecutar la consulta en Prolog
        prolog_output = ejecutar_prolog("rules_prolog.pl", prolog_query)

        # Imprimir la salida cruda de Prolog para depuración
        print(f"Salida cruda de Prolog: {prolog_output}")

        # Procesar la salida
        if "true" in prolog_output:
            return True
        elif "false" in prolog_output:
            return False
        else:
            raise HTTPException(status_code=500, detail=f"Respuesta inesperada de Prolog: {prolog_output}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
