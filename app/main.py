from fastapi import FastAPI

from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router


# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)


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