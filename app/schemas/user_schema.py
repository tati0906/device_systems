from pydantic import BaseModel, EmailStr, Field
from typing import Literal


# Modelo para crear usuarios (POST /users)
class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del usuario"
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool


# Modelo de respuesta de usuario
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool


# Modelo para respuestas estandarizadas
class UserMessage(BaseModel):
    message: str
    user: UserResponse