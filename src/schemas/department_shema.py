from pydantic import BaseModel
from sesc_auth_sdk.enums.department import Department


class DepartmentRequest(BaseModel):
    department: Department