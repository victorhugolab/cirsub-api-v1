import os
import pyodbc
from inflection import underscore, camelize

SP_SUFFIXES = ['OU', 'EL', 'AC', 'IN', 'OT']

SQL_TO_PYTHON = {
    'int': 'int', 'smallint': 'int', 'tinyint': 'int', 'bigint': 'int',
    'bit': 'bool', 'decimal': 'float', 'numeric': 'float', 'float': 'float',
    'real': 'float', 'money': 'float', 'smallmoney': 'float', 'varchar': 'str',
    'nvarchar': 'str', 'text': 'str', 'ntext': 'str', 'char': 'str', 'nchar': 'str',
    'datetime': 'str', 'date': 'str', 'time': 'str', 'timestamp': 'str', 'uniqueidentifier': 'str',
}

def get_connection():
    server = '192.168.1.3'
    database = 'CIRSUB'
    username = 'sa'
    password = 'c17SubDb.2025$!'
    driver = '{ODBC Driver 18 for SQL Server}'

    conn_str = (
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def buscar_sps(tabla: str):
    like_pattern = f'{tabla}_%'
    query = """
    SELECT name FROM sys.objects 
    WHERE type = 'P' AND name LIKE ?;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, [like_pattern])
        return [row[0] for row in cursor.fetchall() if row[0].split('_')[-1] in SP_SUFFIXES]

def obtener_parametros_sp(nombre_sp: str):
    query = """
    SELECT p.name AS parameter_name, TYPE_NAME(p.user_type_id) AS parameter_type, p.is_output, p.parameter_id
    FROM sys.parameters p
    WHERE p.object_id = OBJECT_ID(?)
    ORDER BY p.parameter_id
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, [nombre_sp])
        cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

def generar_modelo(nombre_sp: str, tabla: str):
    parametros = obtener_parametros_sp(nombre_sp)
    if not parametros:
        print(f"⚠️  SP {nombre_sp} no tiene parámetros o no existe.")
        return

    sufijo = nombre_sp.split('_')[-1].lower()
    base_name = f"{tabla}_{sufijo}"
    class_base = camelize(base_name)

    os.makedirs("app/models", exist_ok=True)
    file_path = os.path.join("app/models", f"{base_name}_model.py")

    lines = [
        "from pydantic import BaseModel",
        "from typing import Optional",
        "",
        f"class {class_base}InModel(BaseModel):"
    ]

    for p in parametros:
        if p['is_output']:
            continue
        nombre = p['parameter_name'].lstrip('@')
        tipo_py = SQL_TO_PYTHON.get(p['parameter_type'].lower(), 'str')
        lines.append(f"    {nombre}: {tipo_py}")

    lines.append("")
    lines.append(f"class {class_base}OuModel(BaseModel):")
    lines.append("    mensaje: str  # ajustar según salida real")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Modelo generado: {file_path}")

def generar_controlador(nombre_sp: str, tabla: str):
    sufijo = nombre_sp.split('_')[-1].lower()
    base_name = f"{tabla}_{sufijo}"
    class_base = camelize(base_name)
    model_in = f"{class_base}InModel"

    os.makedirs("app/controllers", exist_ok=True)
    file_path = os.path.join("app/controllers", f"{base_name}_controller.py")

    lines = [
        "from fastapi import Request",
        f"from app.models.{base_name}_model import {model_in}",
        "from app.helpers.db_helper import ejecutar_sp",
        "",
        f"async def {base_name}_controller(request: Request, body: {model_in}):",
        "    params = list(body.dict().values())",
        f"    result = ejecutar_sp('{nombre_sp}', params)",
        "    return result"
    ]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Controlador generado: {file_path}")

def generar_ruta(tabla: str, sps: list):
    base_name = underscore(tabla.lower())
    os.makedirs("app/routers", exist_ok=True)
    file_path = os.path.join("app/routers", f"{base_name}_router.py")

    imports = []
    endpoints = []

    for sp in sps:
        sufijo = sp.split('_')[-1].lower()
        base = f"{tabla}_{sufijo}"
        imports.append(f"from app.controllers.{base}_controller import {base}_controller")
        endpoints.append(
            f"@router.post('/{sufijo}')\n"
            f"async def {base}_endpoint(request: Request, body: dict):\n"
            f"    return await {base}_controller(request, body)"
        )

    lines = [
        "from fastapi import APIRouter, Request",
        *imports,
        "",
        f"router = APIRouter(prefix='/{base_name}', tags=['{tabla}'])",
        ""
    ] + endpoints

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines))

    print(f"✅ Ruta generada: {file_path}")

def main():
    tabla = input("📝 Ingresá el nombre de la tabla: ").strip()
    if not tabla:
        print("❌ Nombre inválido.")
        return

    sps_encontrados = buscar_sps(tabla)
    if not sps_encontrados:
        print(f"❌ No se encontraron SPs con prefijo {tabla}_")
        return

    print(f"🔍 SPs encontrados: {', '.join(sps_encontrados)}")

    for sp in sps_encontrados:
        generar_modelo(sp, tabla)
        generar_controlador(sp, tabla)

    generar_ruta(tabla, sps_encontrados)

if __name__ == "__main__":
    main()
