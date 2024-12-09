from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.estancia_schema import EstanciaResponse, EstanciaCreate, EstanciaUpdate
from models.estancia_model import Estancia
from connection import ejecutar_prolog, get_db

router = APIRouter()

# Crear una nueva estancia
@router.post("/crear_estancia", response_model=EstanciaResponse)
def crear_estancia(estancia: EstanciaCreate, db: Session = Depends(get_db)):
    nueva_estancia = Estancia(**estancia.model_dump())
    db.add(nueva_estancia)
    db.commit()
    db.refresh(nueva_estancia)
    return nueva_estancia

# Obtener todas las estancias
@router.get("/get_estancias")
def get_estancias():
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", "get_estancias")

        estancias = []
        for linea in prolog_output.split("\n"):
            if linea.strip():
                try:
                    (id_estancia, id_detalle_mascota, id_cuarto, inicio_estancia, 
                     fin_estancia, importe) = linea.split(",")

                    estancias.append({
                        "id": int(id_estancia.strip()),
                        "id_detalle_mascota": int(id_detalle_mascota.strip()),
                        "id_cuarto": int(id_cuarto.strip()),
                        "inicio_estancia": inicio_estancia.strip(),
                        "fin_estancia": fin_estancia.strip(),
                        "importe": float(importe.strip())
                    })
                except ValueError:
                    continue

        return estancias
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener una estancia por ID
@router.get("/get_estancia_by_id/{id}")
def get_estancia_by_id(id: int):
    try:
        prolog_output = ejecutar_prolog("rules_prolog.pl", f"get_estancia_by_id({id})")
        print(f"Salida cruda de Prolog: {prolog_output}")

        estancia = None
        for linea in prolog_output.split("\n"):
            linea = linea.strip()
            if linea:
                try:
                    (id_estancia, id_detalle_mascota, id_cuarto, inicio_estancia, 
                     fin_estancia, importe) = linea.split(",")

                    estancia = {
                        "id": int(id_estancia.strip()),
                        "id_detalle_mascota": int(id_detalle_mascota.strip()),
                        "id_cuarto": int(id_cuarto.strip()),
                        "inicio_estancia": inicio_estancia.strip(),
                        "fin_estancia": fin_estancia.strip(),
                        "importe": float(importe.strip())
                    }
                    break
                except ValueError as e:
                    print(f"Error al procesar línea: {linea} -> {e}")
                    continue

        if estancia:
            return estancia
        else:
            raise HTTPException(status_code=404, detail="Estancia no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar una estancia
@router.patch("/actualizar_estancia/{id}", response_model=EstanciaResponse)
def actualizar_estancia(id: int, estancia_actualizada: EstanciaUpdate, db: Session = Depends(get_db)):
    estancia = db.query(Estancia).filter(Estancia.id == id).first()
    if not estancia:
        raise HTTPException(status_code=404, detail="Estancia no encontrada")

    if estancia_actualizada.importe is not None:
        estancia.importe = estancia_actualizada.importe

    db.commit()
    db.refresh(estancia)
    return estancia

# Eliminar una estancia
@router.delete("/eliminar_estancia/{id}", response_model=dict)
def eliminar_estancia(id: int, db: Session = Depends(get_db)):
    estancia = db.query(Estancia).filter(Estancia.id == id).first()
    if not estancia:
        raise HTTPException(status_code=404, detail="Estancia no encontrada")

    db.delete(estancia)
    db.commit()
    return {"message": "Estancia eliminada correctamente"}
