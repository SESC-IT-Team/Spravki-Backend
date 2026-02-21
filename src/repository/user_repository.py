from src.schemas.user_schema import UserSchema

class UserRepository:
    ...


def get_user_repository() -> UserRepository:
    return UserRepository()