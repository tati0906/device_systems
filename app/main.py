from fastapi import FastAPI

from app.routes.user_routes import router as user_router

app = FastAPI(
    title="Device Systems API",
    description="""
API REST para la gestión de usuarios del sistema Device Systems.

Permite:

- Crear usuarios
- Listar usuarios
- Consultar usuarios por ID
- Filtrar usuarios
- Actualizar usuarios
- Eliminar usuarios

Desarrollada con FastAPI y Pydantic v2.
""",
    version="2.0.0",
    contact={
        "name": "Tatiana Vanegas",
        "email": "tatiana@example.com"
    }
)


@app.middleware("http")
async def add_custom_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

    return response


@app.get("/")
def home():

    return {
        "message": "Bienvenido a Device Systems API"
    }


app.include_router(user_router)