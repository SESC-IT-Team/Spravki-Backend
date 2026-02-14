from fastapi import Request

from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.user_schemas import LoginSchema
from src.services.user_services import UserService, get_user_service
router = APIRouter()

@router.post("/login")
async def login(data: LoginSchema, service: UserService = Depends(get_user_service)):
    return service.login(data)

@router.get("/")
async def get_references():
    pass

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