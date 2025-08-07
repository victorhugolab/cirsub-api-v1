from fastapi import APIRouter, Request, Body
from models.Personas.Personas_models import (
    PersonasCbuModel,
    PersonasOUInModel,
    PersonasINModel
)
from controllers.Personas.Personas_controller import (
    personas_controller_CBU,
    personas_controller_ou,
    personas_controller_in,
)
router = APIRouter(prefix="/personas", tags=["Personas"])


@router.post("/ou",summary="Obtener un persona ingresando su ID", response_model=None)
async def personas_ou(request: Request, body: PersonasOUInModel = Body(...)):
    return await personas_controller_ou(request, body)


@router.post("/in", summary="Insertar un registro en Personas", response_model=None)
async def personas_ou(request: Request, body: PersonasINModel = Body(...)):
    return await personas_controller_in(request, body)

@router.post("/cbu", summary="Inserta un CBU en Personas_cbu", response_model=None)
async def personas_ou(request: Request, body: PersonasCbuModel = Body(...)):
    return await personas_controller_CBU(request, body)

