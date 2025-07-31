from fastapi import APIRouter, Request, Query
from typing import Optional
from  controllers import generic_controller

router = APIRouter()

# Búsqueda por campo
@router.get("/personas/buscar")
async def buscar_por_documento(request: Request, campo: str = Query(...), valor: str = Query(...)):
    return await generic_controller.buscar_por_campo(request, "Personas", campo, valor)

# Filtros múltiples
@router.get("/personas/filtros")
async def buscar_con_filtros(request: Request, tipo_documento: Optional[int] = None, apellido: Optional[str] = None):
    filtros = {
        "tipo_documento": tipo_documento,
        "apellido": apellido
    }
    filtros = {k: v for k, v in filtros.items() if v is not None}
    return await generic_controller.buscar_con_filtros(request, "Personas", filtros)

# Paginado
@router.get("/personas/paginado")
async def paginado(request: Request, pagina: int = 1, limite: int = 10):
    return await generic_controller.obtener_paginado(request, "Personas", pagina, limite)
