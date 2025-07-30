import os
import pyodbc
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response  
from settings import settings

from routes.route_personas import router as persona_router 
from routes.route_sp_login import router as login_router
from middlewares.logging_middleware import log_requests  
from middlewares.ip_whitelist_middleware import ip_whitelist
from helpers.error_handler import generic_exception_handler 
from helpers.tools import get_client_ip 
from settings import settings
from database.db import get_connection  

app = FastAPI(title="API CIRSUBGNA-GESTION", version="1.0.0",
    description="Departamento informática CIRSUB GNA. (Arangue, Lopes, Rial)",
    contact={
        "name": "Soporte API",
        "email": "victorh.rial@cirsubgn.org",
        })

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return  Response(content=b"", media_type="image/x-icon")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.middleware("http")(ip_whitelist)
#app.middleware("http")(log_requests)
app.add_exception_handler(Exception, generic_exception_handler)


app.include_router(persona_router, prefix="/api/v1")
app.include_router(login_router , prefix="/api/v1")

# Ejecutar sin parámetros
#resultado, status = ejecutar_sp("SP_GetPersonas")
# Ejecutar con parámetros
#resultado, status = ejecutar_sp("SP_GetPersonaById", [1])
#pip freeze > requirements.txt
#docker-compose up -> para correr local
#docker build -t api-lab-v1:latest .  -> regenera .tar
#docker save -o api-lab-v1.tar api-lab-v1:latest -> guarda el .tar

#| Acción               | Comando                                  |
#| -------------------- | ---------------------------------------- |
#| Levantar servicio    | `docker compose up -d lab-service`       |
#| Ver logs             | `docker logs -f api-lab-v1` (contenedor) |
#| Entrar al contenedor | `docker exec -it api-lab-v1 bash`        |
#| Parar servicio       | `docker compose stop lab-service`        |
#| Reiniciar servicio   | `docker compose restart lab-service`     |


@app.get("/")
async def root(request: Request):
    ip_client = get_client_ip(request)
    environment = os.getenv("ENVIRONMENT", "desconocido")
    return {"message": f"✅ CIRSUB - api-lab-v1 - IP env: {environment} - ipClient {ip_client}", "status": "ok"}


@app.get("/db-test")
async def db_test(request: Request):
    ip_client = get_client_ip(request)
    environment = os.getenv("ENVIRONMENT", "desconocido")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        return {
            "message": f"✅ Conexión DB ok. Desde IP {ip_client} (env: {environment})",
            "status": "ok",
            "result": result[0] if result else None
        }

    except pyodbc.Error as e:
        # Extraer todos los detalles del error
        error_details = {
            "sqlstate": None,
            "code": None,
            "message": str(e),
            "full_args": [],
        }

        # pyodbc.Error.args puede tener (sqlstate, message) o más
        if e.args:
            error_details["full_args"] = [str(arg) for arg in e.args]
            if len(e.args) >= 2:
                error_details["sqlstate"] = e.args[0]
                error_details["code"] = e.args[1]

        # Solo mostrar detalles técnicos si el entorno es local
        response = {
            "message": f"❌ Error de conexión a la base de datos desde IP {ip_client} (env: {environment})",
            "status": "error",
            "error": error_details["message"]
        }

        if environment == "local":
            response["debug"] = error_details

        return response

    except Exception as e:
        return {
            "message": f"❌ Error inesperado desde IP {ip_client} (env: {environment})",
            "status": "error",
            "error": str(e)
        }