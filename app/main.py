from fastapi import FastAPI

from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router

from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear tablas automáticamente

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios usando FastAPI y SQLAlchemy",
    version="3.0.0",
    contact={
        "name": "Tatiana Vanegas"
    }
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a device_systems API"
    }


app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)