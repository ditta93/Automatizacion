import logging
import pyodbc

# Configurar logs para trazabilidad
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ejecutar_proceso():
  connection_string = (
      "DRIVER={ODBC Driver 18 for SQL Server};"
      "SERVER=127.0.0.1,1433;"
      "DATABASE=erp_produccion;"
      "UID=sa;"
      "PWD=TuPasswordSeguro123!;"
      "TrustServerCertificate=yes;"
  )

  try:
    logging.info(
        "Conectando a SQL Server para extraer transacciones pendientes..."
    )
    conexion = pyodbc.connect(connection_string)
    cursor = conexion.cursor()

    # Ejecutando el Procedimiento Almacenado
    cursor.execute("EXEC sp_ObtenerTransaccionesPendientes")
    filas = cursor.fetchall()

    logging.info(
        f"¡Éxito! Se encontraron {len(filas)} registros pendientes en la base"
        " de datos."
    )

    for fila in filas:
      print(
          f"-> ID: {fila.id_transaccion} | Cliente: {fila.cliente} | Monto:"
          f" ${fila.total} | Estado: {fila.estado}"
      )

    conexion.close()

  except Exception as e:
    logging.error(f"Ocurrió un error al ejecutar el proceso: {e}")


if __name__ == "__main__":
  ejecutar_proceso()
