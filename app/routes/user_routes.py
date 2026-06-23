from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status
)

from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.dependencies.database_dependency import get_db

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    patch_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# GET ALL USERS
@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los usuarios"
)
def read_users(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    order_by: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_users(
        db,
        role,
        is_active,
        order_by
    )


# GET USER BY ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID"
)
def read_user(
    user_id: int,
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


# CREATE USER POST
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario"
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


# PUT USER
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
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


# PATCH USER
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcial"
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


# DELETE USER
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario"
)
def delete_existing_user(
    user_id: int,
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