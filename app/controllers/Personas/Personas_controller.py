from fastapi import Request
from database.db_helpers import ejecutar_sp
from helpers.response_helper import success_response, error_response
from models.Personas.Personas_models import PersonasOUInModel, PersonasINModel

#PERSONAS_OU
async def personas_controller_ou(request: Request, body: PersonasOUInModel):
    try:
        params = list(body.model_dump().values())  # convierte el input a lista de valores
        result = ejecutar_sp("Personas_OU", params)
        return success_response(result, "OK")
    except Exception as e:
        return error_response(str(e), status_code=500)

#PERSONAS_IN
async def personas_controller_in(request: Request, body: PersonasINModel):
    try:
        params = list(body.model_dump().values())  # convierte el input a lista de valores
        result = ejecutar_sp("Personas_IN", params)
        return success_response(result, "OK")
    except Exception as e:
        return error_response(str(e), status_code=500)

#PERSONAS_IN
async def personas_controller_CBU(request: Request, body: PersonasINModel):
    try:
        params = list(body.model_dump().values())  # convierte el input a lista de valores
        result = ejecutar_sp("[sp_Personas_Cuentas_banco_CBU_AC]", params)
        return success_response(result, "OK")
    except Exception as e:
        return error_response(str(e), status_code=500)

