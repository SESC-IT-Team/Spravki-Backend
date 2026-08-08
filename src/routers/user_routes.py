from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi import Depends
from sesc_auth_sdk.enums.scope import Scope
from sesc_auth_sdk.dependencies import LyceumAuth, create_jwks_manager_dependency
from sesc_auth_sdk.routers.auth_router import create_auth_router
from sesc_auth_sdk.schemas.user import User
from sesc_auth_sdk.services.jwks_manager import JWKSManager
from sesc_auth_sdk.settings import TokenValidationSettings

from src.dependecies.auth import Auth
from src.schemas.DownloadSchema import DownloadSchema
from src.schemas.HeadersSchema import HeadersSchema
from src.schemas.department_shema import DepartmentRequest
from src.schemas.filter_shema import FilterRequest, FilterShema
from src.schemas.order_shema import OrderShema
from src.services.order_service import OrderService, get_order_service
from src.services.user_service import UserService, get_user_service

router = APIRouter()

@router.post("/create_order")
async def create_order(data: dict, user: Annotated[User, Depends(Auth([Scope.spravki_orders_create]).return_user)], headers: HeadersSchema, order_service: OrderService = Depends(get_order_service)):
    await order_service.create_certificate(headers=headers, data=user, order_data=data)


@router.get("/my_orders")
async def get_my_orders(user: Annotated[User, Depends(Auth([Scope.spravki_orders_get_my]).return_user)], department: DepartmentRequest = Depends(), order_service: OrderService = Depends(get_order_service)) -> list[OrderShema]:
    return await order_service.get_my_orders(department=department, user=user)

@router.get("/orders")
async def get_orders(user: Annotated[User, Depends(Auth([Scope.spravki_orders_get]).return_user)], data: FilterRequest = Depends(), order_service: OrderService = Depends(get_order_service)) -> list[OrderShema]:
    if data is None:
        data = FilterRequest(filter=FilterShema.date_desc)
    return await order_service.get_orders(data=data, user=user)

@router.post("/download")
async def create_document(data: DownloadSchema, user: Annotated[User, Depends(Auth([Scope.spravki_orders_get]).return_user)], service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service)):
    await order_service.create_document(user=user, order_id=data.order_id)

