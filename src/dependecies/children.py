from fastapi import Depends, HTTPException, status
from pydantic import TypeAdapter, ValidationError
from sesc_auth_sdk.enums import Department, Role
from sesc_auth_sdk.schemas.user import User

from src.services.requests_service import RequestsService
from src.config import settings
from src.dependecies.auth import Auth
from src.schemas.HeadersSchema import CertificateTypes
from src.schemas.create_shema import CreateShema
from src.schemas.HeadersSchema import HeadersSchema


async def get_current_user_children_by_cert_type(
    certificate_type: CertificateTypes,
    token: str = Depends(Auth().return_token),
    current_user: User = Depends(Auth().return_user),
) -> list[User]:
    if Role.student in current_user.roles:
        if certificate_type == CertificateTypes.Hostel:
            return []
        users = [current_user]
    elif Role.parent in current_user.roles:
        if certificate_type in (CertificateTypes.Standard, CertificateTypes.Tax, CertificateTypes.MilitaryRegistration, CertificateTypes.SocialFoundation):
            return []
        response = await RequestsService.authorized_request(
            settings.user_service_url + "/v1/users/me/children",
            token
        )
        users_data = response.get("users", response) if isinstance(response, dict) else response
        try:
            users = TypeAdapter(list[User]).validate_python(users_data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="User service returned invalid children data.",
            ) from error
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must have student or parent role.",
        )

    if certificate_type == CertificateTypes.Hostel:
        return [user for user in users if user.lives_in_dormitory]
    return users


async def get_current_user_children_by_dept(
    department: Department,
    token: str = Depends(Auth().return_token),
    current_user: User = Depends(Auth().return_user),
) -> list[User]:
    if Role.student in current_user.roles:
        if department == Department.dormitory:
            return []
        users = [current_user]
    elif Role.parent in current_user.roles:
        if department == Department.educational_department:
            return []
        response = await RequestsService.authorized_request(
            settings.user_service_url + "/v1/users/me/children",
            token,
        )
        users_data = response.get("users", response) if isinstance(response, dict) else response
        try:
            users = TypeAdapter(list[User]).validate_python(users_data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="User service returned invalid children data.",
            ) from error
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must have student or parent role.",
        )

    if department == Department.dormitory:
        return [user for user in users if user.lives_in_dormitory]
    return users

async def check_creation_access(child_id: CreateShema, headers: HeadersSchema, current_user: User = Depends(Auth().return_user), token: str = Depends(Auth().return_token)):
    if Role.student in current_user.roles:
        if child_id.child_id != current_user.id or headers.certificate_type == CertificateTypes.Hostel:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student can only create orders for themselves.",
            )
        return current_user
    elif Role.parent in current_user.roles:
        if headers.certificate_type in (CertificateTypes.Standard, CertificateTypes.Tax, CertificateTypes.MilitaryRegistration, CertificateTypes.SocialFoundation):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Parent cannot create orders for this certificate type.",
            )
        response = await RequestsService.authorized_request(
            settings.user_service_url + f"/v1/users/me/children/{child_id.child_id}",
            token,
        )
        return TypeAdapter(User).validate_python(response)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must have student or parent role.",
        )
