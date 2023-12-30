from typing import Any

from model.user import User


def db_user(db_obj: dict[str, Any]) -> User | None:
    if db_obj is None:
        return None

    return User(
        db_obj['first_name'],
        db_obj['last_name'],
        db_obj['address'],
        db_obj['email'],
        db_obj['date_of_birth'],
        db_obj['pass_hash'],
        db_obj['phone_number'],
        db_obj['is_staff'],
        db_obj['is_admin'],
        db_obj['is_manager'],
        db_obj['id'],
    )
