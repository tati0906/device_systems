from fastapi import APIRouter, HTTPException, Query
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserMessage
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Base de datos temporal en memoria
users_db = [
    {
        "id": 1,
        "name": "Tatiana",
        "email": "tatiana@gmail.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Carlos",
        "email": "carlos@gmail.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Maria",
        "email": "maria@gmail.com",
        "role": "user",
        "is_active": False
    }
]


# GET /users
# Listar todos los usuarios o filtrar por rol y estado
@router.get("/", response_model=list[UserResponse])
def get_users(
    role: str | None = Query(None),
    is_active: bool | None = Query(None)
):
    filtered_users = users_db

    if role is not None:
        filtered_users = [
            user
            for user in filtered_users
            if user["role"] == role
        ]

    if is_active is not None:
        filtered_users = [
            user
            for user in filtered_users
            if user["is_active"] == is_active
        ]

    return filtered_users


# GET /users/{user_id}
# Buscar usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# POST /users
# Crear nuevo usuario
@router.post("/", response_model=UserMessage, status_code=201)
def create_user(user: UserCreate):

    # Validar correo duplicado
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    # Generar ID automático
    new_id = len(users_db) + 1

    # Crear usuario
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    # Guardar usuario
    users_db.append(new_user)

    return {
        "message": "Usuario creado correctamente",
        "user": new_user
    }