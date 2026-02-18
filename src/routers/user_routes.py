from fastapi import Request
from src.services.auth_service import AuthService, get_auth_service
from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.user_schema import LoginSchema
from src.schemas.order_shema import CertificateRequest
from src.services.user_service import UserService, get_user_service
from src.services.order_service import OrderService, get_order_service

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


@router.post("/create_order")
async def create_order(data: CertificateRequest, request: Request, service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service())):
    info = service.get_info(request)
    return order_service.create_certificate(data, info)
