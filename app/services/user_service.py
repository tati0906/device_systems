from app.data.users_db import users_db


def get_all_users():
    return users_db


def get_user_by_id(user_id: int):

    for user in users_db:

        if user["id"] == user_id:
            return user

    return None


def email_exists(
    email: str,
    exclude_user_id: int = None
):

    for user in users_db:

        if exclude_user_id is not None:

            if user["id"] == exclude_user_id:
                continue

        if user["email"] == email:
            return True

    return False


def update_user(
    user_id: int,
    data: dict
):

    for index, user in enumerate(users_db):

        if user["id"] == user_id:

            users_db[index] = {
                "id": user_id,
                **data
            }

            return users_db[index]

    return None


def patch_user(
    user_id: int,
    data: dict
):

    for user in users_db:

        if user["id"] == user_id:

            user.update(data)

            return user

    return None


def delete_user(user_id: int):

    for index, user in enumerate(users_db):

        if user["id"] == user_id:

            deleted_user = users_db.pop(index)

            return deleted_user

    return None