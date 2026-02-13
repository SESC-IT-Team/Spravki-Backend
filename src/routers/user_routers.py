from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.user_schemas import LoginSchema
from src.services.user_services import UserService, get_user_service
router = APIRouter()

@router.post("/login")
async def login(data: LoginSchema, service: UserService = Depends(get_user_service)):
    return service.login(data)
