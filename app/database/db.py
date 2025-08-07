# app/db.py

import pyodbc
from  settings import settings

def get_connection():
    conn_str = (
        f"DRIVER={{{settings.DB_DRIVER}}};"
        f"SERVER={settings.DB_HOST};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD};"
        f"Encrypt=no;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
    )
    try:
        return pyodbc.connect(conn_str, timeout=5)
    except pyodbc.Error as e:
        print("❌ Error de conexión con SQL Server:", e)
        raise
