from enum import Enum
from pydantic import BaseModel


class FilterShema(str, Enum):
    date_asc = "date_asc"
    date_desc = "date_desc"
    status_true = "status_true"
    status_false = "status_false"


class FilterRequest(BaseModel):
    filter: FilterShema