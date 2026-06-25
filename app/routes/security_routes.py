from fastapi import APIRouter, Depends

from app.dependencies.auth_dependency import (
    get_current_active_user
)

router = APIRouter(
    prefix="/security",
    tags=["Security"]
)

@router.get(
    "/profile",
    summary="Perfil del usuario autenticado",
    responses={
        401: {
            "description": "No autenticado"
        },
        403: {
            "description": "Acceso denegado"
        }
    }
)
def get_profile(
    current_user=Depends(get_current_active_user)
):
    return current_user