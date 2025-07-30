from fastapi import Request, Path
from helpers.tools import get_client_ip
from app.database.db_helpers import ejecutar_sp
from app.helpers.response_helper import success_response, error_response
from app.models.persona import PersonaBase
from app.helpers.logger import log_to_file

async def persona_controller_Personas_OT(request: Request):
    client_ip = get_client_ip(request)
    log_to_file("act", "Ejecutando SP: sp_Persona_OT", ip=client_ip)
    result, status = ejecutar_sp("sp_Persona_OT")
    if status != 200 or not result:
        return error_response("No se encontraron personas", 404)
    return success_response(result, "data ok")

async def persona_controller_Persona_OU(id: int, request: Request):
    client_ip = get_client_ip(request)
    log_to_file("act", f"Ejecutando SP: Personas_OU {id}", ip=client_ip)
    result, status = ejecutar_sp("Personas_OU", [id])
    if status != 200 or not result:
        return error_response(f"No se encontró persona con id {id}", 404)
    return success_response(result, "data ok")

async def persona_controller_Persona_IN(request: Request, persona: PersonaBase):
    client_ip = get_client_ip(request)
    log_to_file("act", "Ejecutando SP: Personas_IN", ip=client_ip)
    params = [persona.documento, persona.apellido, persona.nombre, persona.tipo_documento]
    result, status = ejecutar_sp("Personas_IN", params)
    if status != 200:
        return error_response("Error al crear persona", status)
    return success_response(result, "data ok")

async def persona_controller_Persona_AC(id: int, request: Request, persona: PersonaBase):
    client_ip = get_client_ip(request)
    log_to_file("act", f"Ejecutando SP: Personas_AC {id}", ip=client_ip)
    params = [id, persona.documento, persona.apellido, persona.nombre, persona.tipo_documento]
    result, status = ejecutar_sp("Personas_AC", params)
    if status != 200:
        return error_response(f"Error al actualizar persona con id {id}", status)
    return success_response(result, "data ok")

async def persona_controller_Persona_EL(id: int, request: Request):
    client_ip = get_client_ip(request)
    log_to_file("act", f"Ejecutando SP: Personas_EL {id}", ip=client_ip)
    result, status = ejecutar_sp("Personas_EL", [id])
    if status != 200:
        return error_response(f"Error al borrar persona con id {id}", status)
    return success_response(result, "data ok")
