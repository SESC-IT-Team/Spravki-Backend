from fastapi import Request

from src.schemas.user_schemas import LoginSchema
from src.repository.user_repository import UserRepository, get_user_repository
from fastapi import HTTPException
from fastapi.params import Depends
from src.services.auth_service import AuthService, get_auth_service


class UserService:

    def __init__(self, repository: UserRepository, auth: AuthService):
        self.repository = repository
        self.auth = auth


    def login(self, data: LoginSchema):
        user = self.repository.get_user(data.username)

        if not user or user["password"] != data.password:
            raise HTTPException(status_code=401, detail="Wrong login or password")

        return self.auth.create_token(user.get("full_name"), user.get("class"))

    def get_info(self, request: Request):
        info = self.auth.token_info(request)
        return info


def get_user_service(repository: UserRepository = Depends(get_user_repository), auth: AuthService = Depends(get_auth_service)) -> UserService:
    return UserService(repository=repository, auth=auth)
