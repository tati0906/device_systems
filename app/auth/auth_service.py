from app.services.user_service import (
    create_user,
    authenticate_user
)

from app.auth.security import (
    create_access_token
)


def register_user(
    db,
    user_data
):
    return create_user(
        db,
        user_data
    )


def login_user(
    db,
    email,
    password
):
    user = authenticate_user(
        db,
        email,
        password
    )

    if not user:
        return None

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }