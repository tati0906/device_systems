from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict
)

import re


class UserRegister(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str

    role: str

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value
    ):
        if len(value) < 8:
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres"
            )

        if " " in value:
            raise ValueError(
                "La contraseña no puede tener espacios"
            )

        if not re.search(
            r"[A-Z]",
            value
        ):
            raise ValueError(
                "Debe tener una mayúscula"
            )

        if not re.search(
            r"[a-z]",
            value
        ):
            raise ValueError(
                "Debe tener una minúscula"
            )

        if not re.search(
            r"\d",
            value
        ):
            raise ValueError(
                "Debe tener un número"
            )

        return value


class UserLogin(BaseModel):
    email: EmailStr

    password: str


class Token(BaseModel):
    access_token: str

    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserResponseAuth(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )