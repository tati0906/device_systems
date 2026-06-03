from fastapi import FastAPI, Response
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="Device Systems API",
    description="API REST para gestión de usuarios",
    version="1.0.0"
)


@app.middleware("http")
async def add_custom_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return response


@app.get("/")
def home():
    return {
        "message": "Bienvenido a Device Systems API"
    }


app.include_router(user_router)