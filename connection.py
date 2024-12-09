import subprocess
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://tu_usuario:tu_contraseña@tu_servidor/tu_base_de_datos'
#postgresql es el tipo de base de datos
#en tu_servidor es la ip donde esta tu base de datos, si es en tu maquina escribes localhost

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# Ejecutar archivo de prolog
def ejecutar_prolog(archivo: str, regla: str) -> str:
    try:
        print(f"Ejecutando Prolog con el archivo: {archivo} y la regla: {regla}")

        # Ejecutar el comando Prolog con la consulta directamente
        resultado = subprocess.run(
            ["swipl", "-s", archivo, "-g", regla, "-t", "halt"],  # Usamos -g directamente con la consulta
            capture_output=True,
            text=True
        )

        # Verificar si hubo un error en la ejecución de Prolog
        if resultado.returncode != 0:
            print(f"Error al ejecutar Prolog: {resultado.stderr}")
            raise Exception(f"Error en Prolog: {resultado.stderr}")

        # Depuración adicional
        print(f"Salida bruta de Prolog: {resultado.stdout}")
        print(f"Error de Prolog (stderr): {resultado.stderr}")

        # Si la salida de Prolog contiene 'false' (lo cual es un resultado esperado),
        # simplemente retornar false.
        if "false" in resultado.stdout.strip():
            return "false"
        
        return resultado.stdout.strip()

    except Exception as e:
        print(f"Error al ejecutar Prolog: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al ejecutar Prolog: {str(e)}")