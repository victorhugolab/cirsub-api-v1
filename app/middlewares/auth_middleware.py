from fastapi import Request

async def dummy_auth(request: Request, call_next):
    # Aquí podrías validar token o IP, etc.
    return await call_next(request)
