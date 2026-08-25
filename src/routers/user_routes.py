from typing import Annotated, Optional

from aiostream import await_
from fastapi import APIRouter
from fastapi import Depends
from sesc_auth_sdk.enums.scope import Scope
from sesc_auth_sdk.dependencies import LyceumAuth, create_jwks_manager_dependency
from sesc_auth_sdk.routers.auth_router import create_auth_router
from sesc_auth_sdk.schemas.user import User
from sesc_auth_sdk.services.jwks_manager import JWKSManager
from sesc_auth_sdk.settings import TokenValidationSettings
from sesc_auth_sdk.enums import Department

from src.dependecies.department import check_department_admin, check_department_admin_via_download_schema
from src.schemas.create_shema import CreateShema
from src.dependecies.auth import Auth
from src.schemas.DownloadSchema import DownloadSchema
from src.schemas.HeadersSchema import HeadersSchema, CertificateTypes
from src.schemas.department_shema import DepartmentRequest
from src.schemas.filter_shema import FilterRequest, FilterShema
from src.schemas.order_shema import OrderShema
from src.services.order_service import OrderService, get_order_service
from src.services.user_service import UserService, get_user_service
from src.dependecies.children import get_current_user_children_by_cert_type, get_current_user_children_by_dept, check_creation_access

router = APIRouter()

@router.post("/create_order")
async def create_order(data: dict, child_id: CreateShema, user: Annotated[User, Depends(Auth([Scope.spravki_orders_create]).return_user)], headers: HeadersSchema, order_service: OrderService = Depends(get_order_service), child: User = Depends(check_creation_access)):
    try:
        await order_service.create_certificate(headers=headers, data=user, order_data=data, child=child)
    except Exception as e:
        print(f"Error creating certificate: {e}")
        raise


@router.get("/my_orders")
async def get_my_orders(user: Annotated[User, Depends(Auth([Scope.spravki_orders_get_my]).return_user)], department: DepartmentRequest = Depends(), order_service: OrderService = Depends(get_order_service), children: list[User] = Depends(get_current_user_children_by_dept)) -> list[OrderShema]:
    return await order_service.get_my_orders(department=department, children=children)

@router.get("/orders")
async def get_orders(user: Annotated[User, Depends(Auth([Scope.spravki_orders_get]).return_user)], department: Department, data: FilterRequest = Depends(), order_service: OrderService = Depends(get_order_service), _ = Depends(check_department_admin)) -> list[OrderShema]:
    if data.filter is None:
        data.filter = FilterShema.date_desc
    return await order_service.get_orders(data=data, user=user, department=DepartmentRequest(department=department))

@router.post("/download")
async def create_document(data: DownloadSchema, user: Annotated[User, Depends(Auth([Scope.spravki_orders_get]).return_user)], order_service: OrderService = Depends(get_order_service), _ = Depends(check_department_admin_via_download_schema)):
    await order_service.create_document(user=user, order_id=data.order_id)


@router.get("/get_children")
async def get_children(children: list[User] = Depends(get_current_user_children_by_cert_type)):
    return children 