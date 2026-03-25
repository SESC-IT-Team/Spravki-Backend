from enum import Enum

from pydantic import BaseModel


class DepartmentShema(str, Enum):
    educational = "educational"
    CSD = "CSD"
    hostel = "hostel"

class DepartmentRequest(BaseModel):
    department: DepartmentShema