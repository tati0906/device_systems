from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    Request,
    status
)

from app.core.limiter import limiter

from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
    LoginRequest
)

from app.dependencies.database_dependency import get_db

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    patch_user,
    delete_user,
    get_users_by_role,
    get_users_by_status,
    authenticate_user
)

from app.dependencies.auth_dependency import (
    get_current_active_user
)

from app.dependencies.auth_dependency import (
    get_current_user,
    require_admin
)

from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los usuarios",
    description="Consulta todos los usuarios registrados. Permite filtrar por rol, estado y ordenar resultados.",
    response_description="Lista de usuarios obtenida correctamente.",
    responses={
        401: {
            "description": "No autenticado"
        },
        403: {
            "description": "Acceso denegado"
        }
    }
)
@limiter.limit("30/minute")
def read_users(
    request: Request,
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    order_by: str | None = Query(default=None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_users(
        db,
        role,
        is_active,
        order_by
    )


@router.get(
    "/role/{role}",
    response_model=list[UserResponse],
    summary="Buscar usuarios por rol",
    description="Obtiene todos los usuarios que tienen un rol específico."
)
def read_users_by_role(
    role: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_users_by_role(
        db,
        role
    )


@router.get(
    "/status/{is_active}",
    response_model=list[UserResponse],
    summary="Buscar usuarios por estado",
    description="Obtiene usuarios activos o inactivos."
)
def read_users_by_status(
    is_active: bool,
    db: Session = Depends(get_db)
):
    return get_users_by_status(
        db,
        is_active
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Consulta la información de un usuario mediante su identificador.",
    response_description="Usuario encontrado correctamente.",
    responses={
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def read_user(
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente.",
    responses={
        400: {
            "description": "Correo ya registrado"
        },
        401: {
            "description": "No autenticado"
        },
        403: {
            "description": "Acceso denegado"
        },
        422: {
            "description": "Error de validación"
        }
    }
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Correo ya registrado"
        )

    return create_user(
        db,
        user
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    description="Reemplaza completamente la información de un usuario.",
    response_description="Usuario actualizado correctamente.",
    responses={
        400: {
            "description": "Correo ya registrado"
        },
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    existing_email = get_user_by_email(
        db,
        user_data.email
    )

    if existing_email and existing_email.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Correo ya registrado"
        )

    return update_user(
        db,
        user,
        user_data
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza únicamente los campos enviados.",
    response_description="Usuario actualizado correctamente.",
    responses={
        400: {
            "description": "No se enviaron datos para actualizar"
        },
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def patch_existing_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    return patch_user(
        db,
        user,
        user_data
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema.",
    responses={
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def delete_existing_user(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    delete_user(
        db,
        user
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@router.post(
    "/login",
    summary="Iniciar sesión",
    description="Valida email y contraseña del usuario."
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    return {
        "message": "Login exitoso",
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }
