from fastapi import Request
from fastapi import APIRouter
from fastapi.params import Depends

from src.rabbitmq.tasks.HeadersSchema import HeadersSchema
from src.schemas.order_shema import CertificateRequest
from src.services.user_service import UserService, get_user_service
from src.services.order_service import OrderService, get_order_service

router = APIRouter()


@router.get("/")
async def get_references():
    return


@router.post("/create_order")
async def create_order(headers: HeadersSchema, service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service())):
    await order_service.create_certificate(headers)
