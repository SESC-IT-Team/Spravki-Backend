from fastapi import Request
from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.order_shema import CertificateRequest
from src.services.user_service import UserService, get_user_service
from src.services.order_service import OrderService, get_order_service

router = APIRouter()


@router.get("/")
async def get_references():
    return


@router.post("/create_order")
async def create_order(data: CertificateRequest, service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service())):
    info = service.get_current_user()
    return order_service.create_certificate(data, info)
