from fastapi import FastAPI
from sqlalchemy import inspect
from connection import Base, engine
from models import cuarto_model, detalle_model, dueño_model, estancia_model, hotel_model, mascota_model  # Importa todos los modelos
from views.hotel_views import router as hoteles_router
from views.dueño_views import router as dueños_router
from views.cuarto_views import router as cuartos_router
from views.mascota_views import router as mascotas_router
from views.detalle_views import router as detalles_router
from views.estancia_views import router as estancias_router

app = FastAPI()

# Verificar si las tablas existen en la base de datos
inspector = inspect(engine)
tables = inspector.get_table_names()

# Si las tablas no existen, se crean
if not tables:
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")
else:
    print("Las tablas ya existen.")

@app.get("/")
def root():
    return {"message": "API is working!"}

app.include_router(hoteles_router, prefix="/hotel")
app.include_router(dueños_router, prefix="/dueño")
app.include_router(cuartos_router, prefix="/cuarto")
app.include_router(mascotas_router, prefix="/mascota")
app.include_router(detalles_router, prefix="/detalle_mascota")
app.include_router(estancias_router, prefix="/estancia")




