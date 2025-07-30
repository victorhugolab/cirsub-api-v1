import os
import pyodbc

def conectar_sqlserver():
    server = os.getenv("DB_HOST", "sql")
    user = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "clave")
    database = os.getenv("DB_NAME", "master")
    port = os.getenv("DB_PORT", "1433")
    driver = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(connection_string, timeout=3)
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None
