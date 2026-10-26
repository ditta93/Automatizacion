from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse
import logging
import os
import pyodbc

# Cargar las variables del archivo .env
load_dotenv()

# Configurar logs básicos
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="ERP Automation API",
    description="API REST y Panel Web para Integración en la Nube",
    version="1.2.0",
)

API_KEY_SECRETA = "MiTokenSecretoERP2026!"

# Obtener la cadena de conexión desde las variables de entorno (.env)
DB_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTIONSTRING")


def obtener_conexion():
  try:
    if not DB_CONNECTION_STRING:
      raise ValueError("La cadena de conexión no está configurada en el .env")
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    return conn
  except Exception as e:
    logging.error(f"Error al conectar a la base de datos: {e}")
    raise HTTPException(
        status_code=500, detail=f"No se pudo conectar a la base de datos: {e}"
    )

@app.get("/", response_class=HTMLResponse)
def servir_panel():
  try:
    # Lee el archivo index.html ubicado dentro de la carpeta templates
    with open("templates/index.html", "r", encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    return (
        "<h3>Error: No se encontró el archivo index.html en la carpeta"
        " templates/</h3>"
    )

# Ruta de prueba rápida para validar la conexión local
@app.get("/test-db")
def test_db():
  conn = obtener_conexion()
  cursor = conn.cursor()
  cursor.execute("SELECT @@VERSION;")
  db_version = cursor.                                                                                                                                                      one()[0]
  conn.close()
  return {
      "status": "Conexión local exitosa a Azure SQL con ODBC 18",
      "version_sql": db_version,
  }                                                                                                           º