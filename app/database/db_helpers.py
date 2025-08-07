import sys
import traceback
from datetime import date, datetime
from database.db import get_connection
from helpers.response_helper import success_response, error_response
from helpers.logger import log_to_file


def convert_dates(obj, seen=None):
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return None  # o "<circular>" si querés marcarlo
    seen.add(obj_id)

    if isinstance(obj, dict):
        return {k: convert_dates(v, seen) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item, seen) for item in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.strftime('%Y-%m-%d')
    return obj


def ejecutar_sp(nombre_sp: str, params: list = []):
    """
    Ejecuta un procedimiento almacenado en SQL Server y devuelve los resultados.
    Maneja múltiples conjuntos de resultados y el número de filas afectadas.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            param_str = ", ".join("?" for _ in params)
            query = f"EXEC {nombre_sp} {param_str}" if param_str else f"EXEC {nombre_sp}"
            
            cursor.execute(query, params)

            all_results = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    all_results.append(rows)
                else:
                    # Captura el número de filas afectadas si no hay descripción (ej. INSERT, UPDATE)
                    all_results.append({"rows_affected": cursor.rowcount})

                if not cursor.nextset():
                    break
            
            conn.commit()

            # Devuelve el primer resultado si solo hay uno, de lo contrario devuelve la lista completa
            final_data = all_results[0] if len(all_results) == 1 else all_results
            
            # Convierte las fechas a formato de cadena antes de devolver los datos
            return convert_dates(final_data)

    except Exception as e:
        # El manejo de errores es muy importante
        tb = traceback.format_exc()
        exc_type, exc_value, exc_tb = sys.exc_info()
        log_to_file(
            action="dbErr",
            message=f"[ejecutar_sp] {nombre_sp} | Error: {str(e)}",
            code=type(e).__name__,
            ip="sin dato"
        )
        # Relanza la excepción para que el endpoint de la API la capture
        raise e

def ejecutar_sp_back(nombre_sp: str, params: list = []):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        param_str = ", ".join("?" for _ in params)
        query = f"EXEC {nombre_sp} {param_str}" if param_str else f"EXEC {nombre_sp}"
        cursor.execute(query, params)

        all_results = []

        while True:
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                all_results.append(rows)
            else:
                all_results.append({"rows_affected": cursor.rowcount})

            if not cursor.nextset():
                break

        conn.commit()

        # final_data = all_results[0] if len(all_results) == 1 else all_results
        return (all_results[0] if len(all_results) == 1 else all_results, 200)
        # return success_response(convert_dates(final_data), "ok")

    except Exception as e:
        tb = traceback.format_exc()
        exc_type, exc_value, exc_tb = sys.exc_info()

        log_to_file(
            action="dbErr",
            message=f"[ejecutar_sp] {nombre_sp} | Error: {str(e)}",
            code=type(e).__name__,
            ip="sin dato"
        )
        return (f"Error ejecutando SP {nombre_sp}: {str(e)}", 500)
