from fastapi import APIRouter, Request, Path
from  controllers.sp_login_controller import sp_login, sp_Perfil_Login, sp_Perfil_completo

router = APIRouter()

@router.get("/sp_login/{documento}", tags=["Login"])
async def login(
    documento: int = Path(..., description="Documento de la persona"),
    request: Request = None
):
    return await sp_login(documento, request)

@router.get("/sp_perfil_login/{documento}", tags=["Login"])
async def login(
    documento: int = Path(..., description="Documento de la persona"),
    request: Request = None
):
    return await sp_Perfil_Login(documento, request)

@router.get("/sp_perfil_completo/{documento}", tags=["Login"])
async def login(
    documento: int = Path(..., description="Documento de la persona"),
    request: Request = None
):
    return await sp_Perfil_completo(documento, request)
