import os
import pyodbc
import sys
from dotenv import load_dotenv

# Cargar archivo de entorno
load_dotenv(".env.local")

# Agregar app/ al path para que funcionen los imports absolutos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response  
from  settings import settings

from  routes.route_personas import router as persona_router 
from  routes.route_sp_login import router as login_router
from  middlewares.logging_middleware import log_requests  
from  middlewares.ip_whitelist_middleware import ip_whitelist
from  helpers.error_handler import generic_exception_handler 
from  helpers.tools import get_client_ip 
from  settings import settings
from  database.db import get_connection  
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse



app = FastAPI(title="API CIRSUBGNA-GESTION", version="1.1.1",
    description="Departamento informática CIRSUB GNA. (Arangue, Lopez, Rial (vhr))",
    contact={
        "name": "Soporte API",
        "email": "victorh.rial@cirsubgn.org",
        },docs_url=None, redoc_url=None, openapi_url="/openapi.json")

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
SECRET_KEY = "slayer" 

@app.get("/")
async def root(request: Request):
    ip_client = get_client_ip(request)
    environment = os.getenv("ENVIRONMENT", "desconocido")
    return {"message": f"✅ CIRSUB - api-lab-v1 - IP env: {environment} - ip-Client {ip_client}", "status": "ok"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    # Validar el parámetro "key"
    key = request.query_params.get("key")
    if key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    client_ip = request.client.host
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"Documentación API - IP: {client_ip}",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )
    return HTMLResponse(content=html.body.decode().replace(
        "<title>Swagger UI</title>",
        f"<title>API - {client_ip}</title>"
    ), status_code=200)

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