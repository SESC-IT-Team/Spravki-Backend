from pydantic import BaseModel
from sesc_auth_sdk.enums.departments import Department


class DepartmentRequest(BaseModel):
    department: Department