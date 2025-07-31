from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from  helpers.tools import get_client_ip
from  helpers.logger import  log_to_file

async def log_requests(request: Request, call_next):
    if request.url.path == "/favicon.ico":
        return await call_next(request)

    method = request.method
    path = request.url.path
    client_ip = get_client_ip(request)

    response = await call_next(request)

    log_to_file(
        action="info",
        message=f"{method} {path}",
        code="null",
        ip=client_ip
    )

    return response
