from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.cuarto_schema import CuartoResponse, CuartoCreate, CuartoUpdate
from models.cuarto_model import Cuarto
from connection import ejecutar_prolog, get_db

router = APIRouter()

@router.post("/crear_cuarto", response_model=CuartoResponse)
def crear_cuarto(cuarto: CuartoCreate, db: Session = Depends(get_db)):
    nuevo_cuarto = Cuarto(**cuarto.model_dump())
    db.add(nuevo_cuarto)
    db.commit()
    db.refresh(nuevo_cuarto)
    return nuevo_cuarto

@router.get("/get_cuartos")
def get_cuartos():
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_cuartos")

        cuartos = []
        for linea in prolog_output.split("\n"):
            if linea.strip():
                try:
                    id_cuarto, id_hotel, numero_cuarto, disponible = linea.split(",")
                    cuartos.append({
                        "id": int(id_cuarto.strip()),
                        "id_hotel": int(id_hotel.strip()),
                        "numero_cuarto": int(numero_cuarto.strip()),
                        "disponible": disponible.strip()
                    })
                except ValueError:
                    # Si hay un error al procesar la línea, omitirla
                    continue

        return cuartos
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Obtener un hotel por ID (GET) - Personaliza la regla en Prolog para este caso
@router.get("/get_cuarto_by_id/{id}")
def get_cuarto_by_id(id: int):
    try:
        # Llamar a Prolog para obtener el cuarto con el ID solicitado
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_cuarto_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")  # Depuración

        # Procesar la salida de Prolog
        cuarto = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:  # Verifica que la línea no esté vacía
                try:
                    # Parsear la línea con formato "1, 1er HOTEL"
                    id_cuarto, id_hotel, numero_cuarto, disponible_str = linea.split(",", maxsplit=3)

                    # Convertir 'disponible' a booleano
                    disponible = True if disponible_str.strip().lower() == "true" else False

                    # Crear el diccionario con los datos del cuarto
                    cuarto = {
                        "id": int(id_cuarto.strip()),
                        "id_hotel": int(id_hotel.strip()),
                        "numero_cuarto": int(numero_cuarto.strip()),
                        "disponible": disponible
                    }
                    break  # Detener el bucle después de encontrar el primer resultado
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if cuarto:
            return cuarto
        else:
            raise HTTPException(status_code=404, detail="Cuarto no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Actualizar un dueño (PATCH)
@router.patch("/actualizar/{id}", response_model=CuartoResponse)
def actualizar_cuarto(id: int, cuarto_actualizado: CuartoUpdate, db: Session = Depends(get_db)):
    cuarto = db.query(Cuarto).filter(Cuarto.id == id).first()
    if not cuarto:
        raise HTTPException(status_code=404, detail="Cuarto no encontrado")
    
    if cuarto_actualizado.numero_cuarto is not None:
        cuarto.numero_cuarto = cuarto_actualizado.numero_cuarto
    if cuarto_actualizado.disponible is not None:
        cuarto_actualizado.disponible = cuarto_actualizado.disponible

@router.delete("/eliminar/{id}", response_model=dict)
def eliminar_cuarto(id: int, db: Session = Depends(get_db)):
    cuarto = db.query(Cuarto).filter(Cuarto.id == id).first()
    if not cuarto:
        raise HTTPException(status_code=404, detail="Cuarto no encontrado")
    
    db.delete(Cuarto)
    db.commit()
    return {"message": "Cuarto eliminado correctamente"}

@router.get("/get_cuartos_disponibles")
def get_cuartos():
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_cuartos_disponibles")

        cuartos = []
        for linea in prolog_output.split("\n"):
            if linea.strip():
                try:
                    id_cuarto, id_hotel, numero_cuarto, disponible = linea.split(",")
                    cuartos.append({
                        "id": int(id_cuarto.strip()),
                        "id_hotel": int(id_hotel.strip()),
                        "numero_cuarto": int(numero_cuarto.strip()),
                        "disponible": disponible.strip()
                    })
                except ValueError:
                    # Si hay un error al procesar la línea, omitirla
                    continue

        return cuartos
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
