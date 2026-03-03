from fastapi import Request
from src.repository.user_repository import UserRepository, get_user_repository
from src.schemas.user_schema import UserSchema
from fastapi.params import Depends



class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_current_user(self) -> UserSchema:
        return UserSchema({
            "id": "c1e8cd06-6748-4a56-9002-403c4c729a58",
            "last_name": "Пупкин",
            "first_name": "Ваня",
            "middle_name": "Петрович",
            "role": "student",
            "gender": "male",
            "class_name": "8Е",
            "graduation_year": "2029",
            "login": "admin",
            "created_at": "2026-02-17T06:17:27.599959Z",
            "updated_at": "2026-02-17T06:17:27.599961Z"
        })

    def check_admin(self):
        ...


def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)
