import sys
import traceback
from app.database.db import get_connection
from app.helpers.response_helper import success_response, error_response
from app.helpers.logger import log_to_file



def ejecutar_sp(nombre_sp: str, params: list = []):
    conn = None  # 👈 importante
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

        return success_response(all_results[0] if len(all_results) == 1 else all_results)

    except Exception as e:
        tb = traceback.format_exc()  # stack trace completo
        exc_type, exc_value, exc_tb = sys.exc_info()

        log_to_file(
            action="err1",
            message=f"[ejecutar_sp] {nombre_sp} | Error: {str(e)}\nTraceback:\n{tb}",
            code=type(e).__name__,
            ip=""
        )

        return error_response(f"Error ejecutando SP {nombre_sp}: {str(e)}", 500)