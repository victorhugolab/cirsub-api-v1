from database.db import get_connection
from helpers.response_helper import success_response, error_response

def ejecutar_sp(nombre_sp: str, params: list = []):
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
                # No hay resultados, pero puede haber rows afectadas
                all_results.append({"rows_affected": cursor.rowcount})

            # Pasar al siguiente result set, si existe
            if not cursor.nextset():
                break

        conn.commit()

        # Si solo hubo un set, devolvemos ese set directamente
        if len(all_results) == 1:
            return success_response(all_results[0])
        return success_response(all_results)

    except Exception as e:
        return error_response(f"Error ejecutando SP {nombre_sp}: {str(e)}", 500)
    finally:
        conn.close()
