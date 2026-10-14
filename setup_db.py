import pyodbc

# Conexión inicial al servidor maestro (usando el usuario 'sa' y la contraseña que pusiste en Docker)
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=127.0.0.1,1433;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=TuPasswordSeguro123!;"
    "TrustServerCertificate=yes;"
)

try:
  conexion = pyodbc.connect(conn_str, autocommit=True)
  cursor = conexion.cursor()
  print("¡Conexión exitosa al servidor SQL Server!")

  # 1. Crear la Base de Datos si no existe
  cursor.execute(
      "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'erp_produccion')"
      " CREATE DATABASE erp_produccion;"
  )
  print("Base de datos 'erp_produccion' lista.")

  conexion.close()

  # 2. Conectar directamente a la nueva base de datos para crear tablas
  conn_db_str = (
      "DRIVER={ODBC Driver 18 for SQL Server};"
      "SERVER=127.0.0.1,1433;"
      "DATABASE=erp_produccion;"
      "UID=sa;"
      "PWD=TuPasswordSeguro123!;"
      "TrustServerCertificate=yes;"
  )
  conexion_db = pyodbc.connect(conn_db_str, autocommit=True)
  cursor_db = conexion_db.cursor()

  # Crear tabla de transacciones
  cursor_db.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='transacciones' and xtype='U')
        CREATE TABLE transacciones (
            id_transaccion INT IDENTITY(1,1) PRIMARY KEY,
            cliente NVARCHAR(100),
            total DECIMAL(18,2),
            estado NVARCHAR(20),
            fecha_creacion DATETIME DEFAULT GETDATE()
        );
    """)
  print("Tabla 'transacciones' creada.")

  # Insertar datos de prueba
  cursor_db.execute(
      "INSERT INTO transacciones (cliente, total, estado) VALUES ('Empresa"
      " Alfa S.A.', 1500.00, 'PENDIENTE');"
  )
  cursor_db.execute(
      "INSERT INTO transacciones (cliente, total, estado) VALUES"
      " ('Comercial Beta', 3200.50, 'PENDIENTE');"
  )
  print("Datos de prueba insertados.")

  # Crear el Procedimiento Almacenado (Eliminamos si existe antes para evitar errores)
  cursor_db.execute("""
        CREATE OR ALTER PROCEDURE sp_ObtenerTransaccionesPendientes
        AS
        BEGIN
            SET NOCOUNT ON;
            SELECT id_transaccion, cliente, total, estado 
            FROM transacciones 
            WHERE estado = 'PENDIENTE';
        END
    """)
  print("Procedimiento almacenado 'sp_ObtenerTransaccionesPendientes' creado.")

  conexion_db.close()

except Exception as e:
  print(f"Error durante la configuración: {e}")
