from fastapi import Request
from fastapi import APIRouter
from fastapi.params import Depends
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema
from src.schemas.order_shema import CertificateRequest
from src.services.user_service import UserService, get_user_service
from src.services.order_service import OrderService, get_order_service
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/")
async def get_references():
    return


@router.post("/create_order")
async def create_order(headers: HeadersSchema, order_service: OrderService = Depends(get_order_service)):
    await order_service.create_certificate(headers)


@router.get("/orders")
async def get_orders(session: AsyncSession = Depends(get_session), order_service: OrderService = Depends(get_order_service)):
    return await order_service.get_orders(session)

@router.get("/create_document")
async def create_document(service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service), session: AsyncSession = Depends(get_session)):
    service.check_admin()
    await order_service.create_document(session)


