from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal

from app.schemas.auth_schema import (
    UserRegister,
    Token,
    UserResponseAuth
)

from app.auth.auth_service import (
    register_user,
    login_user
)

from app.services.user_service import (
    get_user_by_email
)

from app.dependencies.auth_dependency import (
    get_current_user
)

from app.models.user_model import User

from app.core.limiter import limiter

from fastapi import Request

from app.core.limiter import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/register",
    response_model=UserResponseAuth,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserRegister,
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

    return register_user(
        db,
        user
    )


@router.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = login_user(
        db,
        form_data.username,
        form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    return token


@router.get(
    "/me",
    response_model=UserResponseAuth
)
def read_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user

