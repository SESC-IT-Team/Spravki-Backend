from src.schemas.user_schemas import LoginSchema
from src.repository.user_repository import UserRepository, get_user_repository
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from fastapi.params import Depends


SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_token(self, username: str):
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": username, "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def login(self, data: LoginSchema):
        user = self.repository.get_user(data.username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user["password"] != data.password:
            raise HTTPException(status_code=401, detail="Wrong password")

        token = self.create_token(data.username)

        return {"token": token}

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)