from sqlalchemy.orm import Session
from app.models.user_model import User

# Crear usuario
def create_user(db: Session, user_data):
    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# Obtener todos los usuarios
def get_users(
    db: Session,
    role=None,
    is_active=None,
    order_by=None
):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    if order_by == "name":
        query = query.order_by(User.name)

    elif order_by == "created_at":
        query = query.order_by(User.created_at)

    return query.all()


# Buscar usuario por ID
def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

# Buscar usuario por email
def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

# Actualización completa
def update_user(
    db: Session,
    user,
    user_data
):
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user

# Actualización parcial
def patch_user(
    db: Session,
    user,
    user_data
):
    update_data = (
        user_data.model_dump(
            exclude_unset=True
        )
    )

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

# Eliminar usuario
def delete_user(
    db: Session,
    user
):
    db.delete(user)
    db.commit()

# Buscar por rol
def get_users_by_role(
    db: Session,
    role: str
):
    return (
        db.query(User)
        .filter(User.role == role)
        .all()
    )

# Buscar por estado
def get_users_by_status(
    db: Session,
    is_active: bool
):
    return (
        db.query(User)
        .filter(User.is_active == is_active)
        .all()
    )