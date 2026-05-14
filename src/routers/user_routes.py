from fastapi import APIRouter
from fastapi.params import Depends
from src.schemas.HeadersSchema import HeadersSchema
from src.schemas.department_shema import DepartmentRequest
from src.schemas.order_shema import OrderShema
from src.services.user_service import UserService, get_user_service
from src.services.order_service import OrderService, get_order_service
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.filter_shema import FilterRequest
from typing import Annotated
from sesc_auth_sdk.schemas.user import UserSchema
from sesc_auth_sdk.dependencies import LyceumAuth
from sesc_auth_sdk.enums.role import Role
from sesc_auth_sdk.enums.permission import Permissions
router = APIRouter()



@router.post("/create_order")
async def create_order(user: Annotated[UserSchema, Depends(LyceumAuth([Permissions.Spravki.Orders.create]).return_user)], headers: HeadersSchema, order_service: OrderService = Depends(get_order_service)):
    await order_service.create_certificate(headers=headers, data=user)


@router.post("/get_my_orders")
async def get_my_orders(user: Annotated[UserSchema, Depends(LyceumAuth([Permissions.Spravki.Orders.get_my]).return_user)], department: DepartmentRequest, order_service: OrderService = Depends(get_order_service)) -> list[OrderShema]:
    return await order_service.get_my_orders(department=department, user=user)

@router.post("/get_orders")
async def get_orders(user: Annotated[UserSchema, Depends(LyceumAuth([Permissions.Spravki.Orders.get]).return_user)], data: FilterRequest, order_service: OrderService = Depends(get_order_service)) -> list[OrderShema]:
    return await order_service.get_orders(data=data, user=user)

@router.post("/download")
async def create_document(user: Annotated[UserSchema, Depends(LyceumAuth([Permissions.Spravki.Orders.get]).return_user)], service: UserService = Depends(get_user_service), order_service: OrderService = Depends(get_order_service)):
    await order_service.create_document(user=user)


