from fastapi import HTTPException

from app.data.users_db import users_db


def create_error_response(
    message: str,
    status_code: int
):

    raise HTTPException(
        status_code=status_code,
        detail={
            "error": True,
            "message": message,
            "status_code": status_code
        }
    )


def get_user_or_404(user_id: int):

    for user in users_db:

        if user["id"] == user_id:
            return user

    create_error_response(
        "Usuario no encontrado",
        404
    )


def get_api_config():

    return {
        "app_name": "device_systems",
        "version": "2.0.0"
    }