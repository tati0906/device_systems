from fastapi import APIRouter, Query, Depends

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserMessage,
    UserUpdate,
    UserPatch
)

from app.dependencies.user_dependencies import (
    get_user_or_404,
    create_error_response,
    get_api_config
)

from app.services.user_service import (
    email_exists,
    update_user,
    patch_user,
    delete_user
)

from app.data.users_db import users_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene la lista completa de usuarios o permite filtrar por rol y estado.",
    response_description="Lista de usuarios encontrada"
)
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


@router.get(
    "/config/info",
    summary="Información de la API",
    description="Obtiene la configuración general de la API.",
    response_description="Configuración obtenida correctamente"
)
def get_config(
    config=Depends(get_api_config)
):

    return config


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario",
    description="Obtiene la información de un usuario mediante su ID.",
    response_description="Usuario encontrado"
)
def get_user_by_id(user_id: int):

    for user in users_db:

        if user["id"] == user_id:
            return user

    create_error_response(
        "Usuario no encontrado",
        404
    )


@router.post(
    "/",
    response_model=UserMessage,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente"
)
def create_user(user: UserCreate):

    for existing_user in users_db:

        if existing_user["email"] == user.email:

            create_error_response(
                "El correo ya está registrado",
                400
            )

    new_id = len(users_db) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    users_db.append(new_user)

    return {
        "message": "Usuario creado correctamente",
        "user": new_user
    }


@router.put(
    "/{user_id}",
    summary="Actualizar usuario completamente",
    description="Reemplaza completamente la información de un usuario existente.",
    response_description="Usuario actualizado",
    response_model=UserResponse,
    status_code=200
)
def update_user_route(
    user_id: int,
    user_data: UserUpdate,
    existing_user=Depends(get_user_or_404)
):

    if email_exists(
        user_data.email,
        exclude_user_id=user_id
    ):

        create_error_response(
            "El correo ya está registrado",
            400
        )

    updated_user = update_user(
        user_id,
        user_data.model_dump()
    )

    return updated_user


@router.patch(
    "/{user_id}",
    summary="Actualizar parcialmente un usuario",
    description="Modifica únicamente los campos enviados por el cliente.",
    response_description="Usuario actualizado parcialmente",
    response_model=UserResponse,
    status_code=200
)
def patch_user_route(
    user_id: int,
    user_data: UserPatch,
    existing_user=Depends(get_user_or_404)
):

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:

        create_error_response(
            "Debe enviar al menos un campo para actualizar",
            400
        )

    if "email" in update_data:

        if email_exists(
            update_data["email"],
            exclude_user_id=user_id
        ):

            create_error_response(
                "El correo ya está registrado",
                400
            )

    updated_user = patch_user(
        user_id,
        update_data
    )

    return updated_user


@router.delete(
    "/{user_id}",
    summary="Eliminar usuario",
    description="Elimina un usuario existente mediante su ID.",
    response_description="Usuario eliminado correctamente",
    status_code=200
)
def delete_user_route(
    user_id: int,
    existing_user=Depends(get_user_or_404)
):

    delete_user(user_id)

    return {
        "message": "Usuario eliminado correctamente"
    }