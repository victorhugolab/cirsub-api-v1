# test_connection.py

import sys
import os

# Asegurarse de que se pueda importar 'app'
sys.path.append(os.path.dirname(__file__))

from  database.db import get_connection

def main():
    try:
        conn = get_connection()
        print("✅ Conexión exitosa a la base de datos.")
        conn.close()
    except Exception as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)

if __name__ == "__main__":
    main()
