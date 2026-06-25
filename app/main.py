from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.limiter import limiter

from app.middlewares.request_middleware import request_middleware

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from app.routes.security_routes import router as security_router

# TAGS DE SWAGGER
openapi_tags = [
    {
        "name": "Auth",
        "description": "Autenticación y autorización"
    },
    {
        "name": "Users",
        "description": "Gestión de usuarios"
    },
    {
        "name": "Devices",
        "description": "Gestión de dispositivos"
    },
    {
        "name": "Loans",
        "description": "Gestión de préstamos"
    },
    {
        "name": "Security",
        "description": "Seguridad, JWT y control de acceso"
    }
]

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0",
    contact={
        "name": "Tatiana Vanegas"
    },
    openapi_tags=openapi_tags
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

@app.middleware("http")
async def middleware(
    request: Request,
    call_next
):
    return await request_middleware(
        request,
        call_next
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {
        "message": "Bienvenido a device_systems API"
    }

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(auth_router)
app.include_router(security_router)