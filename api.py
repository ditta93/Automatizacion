from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse
import logging
import os
import pyodbc

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


def obtener_conexion():
  try:
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=127.0.0.1,1433;"
        "DATABASE=erp_produccion;"
        "UID=sa;"
        "PWD=TuPasswordSeguro123!;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)
  except Exception as e:
    logging.error(f"Error de conexión a la base de datos: {e}")
    raise HTTPException(
        status_code=500, detail="No se pudo conectar a la base de datos."
    )


# --- 1. RUTA PARA SERVIR EL PANEL VISUAL (FRONTEND) ---
@app.get("/", response_class=HTMLResponse)
def leer_interfaz():
  ruta_html = "templates/index.html"
  if os.path.exists(ruta_html):
    with open(ruta_html, "r", encoding="utf-8") as f:
      return f.read()
  return (
      "<h1>Error: No se encontró el archivo de la interfaz visual en"
      " templates/index.html</h1>"
  )


# --- 2. ENDPOINT SEGURO DE TRANSACCIONES (API REST) ---
@app.get("/transacciones-pendientes")
def get_transacciones(
    estado: str = Query(
        "PENDIENTE", description="Filtro opcional por estado"
    ),
    api_key: str = Header(..., alias="x-api-key"),
):
  if api_key != API_KEY_SECRETA:
    raise HTTPException(status_code=403, detail="API Key no autorizada.")

  try:
    logging.info("Consultando registros en SQL Server...")
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("EXEC sp_ObtenerTransaccionesPendientes")

    columnas = [column[0] for column in cursor.description]
    filas = [dict(zip(columnas, row)) for row in cursor.fetchall()]

    conexion.close()

    return {
        "status": "success",
        "filtro_aplicado": estado,
        "total_registros": len(filas),
        "data": filas,
    }

  except Exception as e:
    logging.error(f"Error al procesar la consulta: {e}")
    raise HTTPException(status_code=500, detail=str(e))