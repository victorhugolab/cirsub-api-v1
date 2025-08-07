from fastapi import Request
from  helpers.tools import get_client_ip
from  database.db_helpers import ejecutar_sp
from  helpers.response_helper import success_response, error_response
from  helpers.logger import log_to_file
from  helpers.tools import parse_json

async def sp_login(documento: int, request: Request):
    client_ip = get_client_ip(request)

    log_to_file(
        action="info",
        message=f"Ejecutando SP: sp_login {documento}",
        ip=client_ip
    )

    result, status = ejecutar_sp("sp_login", [documento])

    if status != 200 or not result:
        return error_response("Credenciales inválidas", 401)

    return success_response(result, "data ok")


async def sp_Perfil_completo(documento: int, request: Request):
    client_ip = get_client_ip(request)

    log_to_file(
        action="info",
        message=f"Ejecutando SP: sp_Perfil_completo {documento}",
        ip=client_ip
    )

    result, status = ejecutar_sp("sp_Perfil_completo", [documento])

    if status != 200 or not result:
        return error_response("Credenciales inválidas", 401)

    if result["data"]:
        data = parse_json(result["data"][0])

    return success_response(data, "data ok")



async def sp_Perfil_Login(documento: int, request: Request):
    client_ip = get_client_ip(request)

    log_to_file(
        action="info",
        message=f"Ejecutando SP: sp_Perfil_Login {documento}",
        ip=client_ip
    )

    result, status = ejecutar_sp("sp_Perfil_Login", [documento])

    if status != 200 or not result:
        return error_response("Credenciales inválidas", 401)

    if result["data"]:
        data = parse_json(result["data"][0])
    

    return success_response(data, "data ok")
