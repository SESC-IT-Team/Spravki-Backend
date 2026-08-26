from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from src.config import settings

from src.dependecies.auth import Auth

from sesc_auth_sdk.enums import Department
from sesc_auth_sdk.schemas.user import User

from src.services.requests_service import RequestsService
from src.services.order_service import OrderService, get_order_service
from src.schemas.DownloadSchema import DownloadSchema
from src.schemas.HeadersSchema import CertificateTypes, HeadersSchema


async def check_department_admin(
    department: Department,
    token: str = Depends(Auth().return_token),
) -> None:
    response = await RequestsService.authorized_request(
        settings.user_service_url
        + f"/v1/departments/{department.value}/members/me",
        token,
        raise_for_status={404: HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin of this department.",
        )}
    )

    if response.get("position") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin of this department.",
        )


async def check_department_admin_via_download_schema(
    data: DownloadSchema,
    token: str = Depends(Auth().return_token),
    order_service: OrderService = Depends(get_order_service),
) -> None:
    order = await order_service.get_order_by_id(order_id=data.order_id)
    department = Department(order.department)
    response = await RequestsService.authorized_request(
        settings.user_service_url
        + f"/v1/departments/{department.value}/members/me",
        token,
        raise_for_status={404: HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin of this department.",
        )}
    )

    if response.get("position") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin of this department.",
        )
