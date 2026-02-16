from fastapi import Request
from src.services.auth_service import AuthService, get_auth_service
from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.user_schema import LoginSchema
from src.services.user_service import UserService, get_user_service
router = APIRouter()

@router.post("/login")
async def login(data: LoginSchema, service: UserService = Depends(get_user_service)):
    return service.login(data)

@router.get("/login")
async def login_screen():
    pass

@router.get("/")
async def get_references(request: Request, service: AuthService = Depends(get_auth_service)):
    return service.token_info(request)


#Сервис отрисовки
@router.post("/reference_1")
async def generate_ref_1(request: Request, service: UserService = Depends(get_user_service)):
    info = service.get_info(request)
    return info

@router.post("/reference_2")
async def generate_ref_2(request: Request, service: UserService = Depends(get_user_service)):
    info = service.get_info(request)
    return info


@router.post("/reference_3")
async def generate_ref_3(request: Request, service: UserService = Depends(get_user_service)):
    info = service.get_info(request)
    return info

@router.post("/reference_4")
async def generate_ref_4(request: Request, service: UserService = Depends(get_user_service)):
    info = service.get_info(request)
    return info