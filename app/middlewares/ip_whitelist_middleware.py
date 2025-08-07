from fastapi import Request
from starlette.responses import JSONResponse
from  helpers.tools import get_client_ip

# Lista blanca de IPs permitidas
ALLOWED_IPS = ["127.0.0.1", "192.168.1.100"]

async def ip_whitelist(request: Request, call_next):
    client_ip = get_client_ip(request)
    if client_ip not in ALLOWED_IPS:
        return JSONResponse(
            content={"status": "error", "message": "Acceso denegado desde esta IP"},
            status_code=403
        )
    return await call_next(request)
