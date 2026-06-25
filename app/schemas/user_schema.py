from typing import Optional, Literal
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator
)



# Crear usuario
class UserCreate(BaseModel):

    name: str = Field(
        min_length=3,
        description="Nombre del usuario"
    )

    email: EmailStr

    password: str = Field(
        min_length=6
    )

    role: Literal["admin", "support", "user"]

    is_active: bool = True


# Actualización completa
class UserUpdate(BaseModel):

    name: str = Field(
        min_length=3
    )

    email: EmailStr

    password: str = Field(
        min_length=6
    )

    role: Literal["admin", "support", "user"]

    is_active: bool


# Actualización parcial
class UserPatch(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=3
    )

    email: Optional[EmailStr] = None

    role: Optional[
        Literal["admin", "support", "user"]
    ] = None

    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.replace(" ", "").isalpha():
            raise ValueError(
                "El nombre solo puede contener letras"
            )
        return value

# Respuesta
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

class LoginRequest(BaseModel):  
    email: str
    password: str