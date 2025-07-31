from fastapi import Request
from typing import Type, Optional, Dict, Any, List
from  helpers.tools import get_client_ip
from  helpers.logger import log_to_file
from  helpers.response_helper import success_response, error_response
from  database.db_helpers import ejecutar_sp

# Funciones básicas ya vistas...

# 🔍 Buscar por campo
async def buscar_por_campo(request: Request, tabla: str, campo: str, valor: Any):
    client_ip = get_client_ip(request)
    sp_name = f"{tabla}_BuscarPorCampo"  # Ej: Personas_BuscarPorCampo
    log_to_file("act", f"Ejecutando SP: {sp_name} con campo {campo} = {valor}", ip=client_ip)
    result, status = ejecutar_sp(sp_name, [campo, valor])
    if status != 200 or not result:
        return error_response(f"No se encontraron resultados en {tabla} con {campo} = {valor}", 404)
    return success_response(result, "data ok")

# 🧩 Búsqueda avanzada con múltiples filtros (requiere SP como Tabla_Filtros)
async def buscar_con_filtros(request: Request, tabla: str, filtros: Dict[str, Any]):
    client_ip = get_client_ip(request)
    sp_name = f"{tabla}_Filtros"
    log_to_file("act", f"Ejecutando SP: {sp_name} con filtros {filtros}", ip=client_ip)
    params = list(filtros.values())  # El orden debe coincidir con el SP
    result, status = ejecutar_sp(sp_name, params)
    if status != 200 or not result:
        return error_response(f"No se encontraron resultados en {tabla} con esos filtros", 404)
    return success_response(result, "data ok")

# 📄 Paginación simple (requiere SP con paginado)
async def obtener_paginado(request: Request, tabla: str, pagina: int = 1, limite: int = 10):
    client_ip = get_client_ip(request)
    sp_name = f"{tabla}_Paginado"
    log_to_file("act", f"Ejecutando SP: {sp_name} (página {pagina}, límite {limite})", ip=client_ip)
    params = [pagina, limite]
    result, status = ejecutar_sp(sp_name, params)
    if status != 200 or not result:
        return error_response(f"No se encontraron resultados en {tabla}", 404)
    return success_response(result, "data ok")
