from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Crear usuario
class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        description="Nombre del usuario"
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool = True


# Actualización completa
class UserUpdate(BaseModel):
    name: str = Field(
        min_length=3
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool


# Actualización parcial
class UserPatch(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=3
    )

    email: Optional[EmailStr] = None

    role: Optional[Literal["admin", "support", "user"]] = None

    is_active: Optional[bool] = None


# Respuesta
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )