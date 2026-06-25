from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal

from app.auth.security import decode_access_token

from app.services.user_service import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(
        db,
        email
    )

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user=Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    return current_user


def require_admin(
    current_user=Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Permisos insuficientes"
        )

    return current_user

def require_admin_or_support(
    current_user=Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="Permisos insuficientes"
        )

    return current_user