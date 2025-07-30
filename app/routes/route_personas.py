from fastapi import APIRouter, Request, Path
from app.controllers.persona_controller import (
    persona_controller_Personas_OT,
    persona_controller_Persona_OU,
    persona_controller_Persona_IN,
    persona_controller_Persona_AC,
    persona_controller_Persona_EL,
)
from app.models.persona import PersonaCreate, PersonaUpdate

router = APIRouter()

@router.get("/personas",tags=["Personas"])
async def get_personas(request: Request):
    return await persona_controller_Personas_OT(request)

@router.get("/personas/{id}",tags=["Personas"])
async def get_persona_by_id(
    id: int = Path(..., description="ID de la persona a buscar"),
    request: Request = None,
):
    return await persona_controller_Persona_OU(id, request)

@router.post("/personas",tags=["Personas"])
async def create_persona(persona: PersonaCreate, request: Request):
    return await persona_controller_Persona_IN(request, persona)

@router.put("/personas/{id}",tags=["Personas"])
async def update_persona(
    id: int,
    persona: PersonaUpdate,
    request: Request,
):
    return await persona_controller_Persona_AC(id, request, persona)

@router.delete("/personas/{id}",tags=["Personas"])
async def delete_persona(
    id: int,
    request: Request,
):
    return await persona_controller_Persona_EL(id, request)
