from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrderShema(BaseModel):
    id: UUID
    number: int
    link: Optional[str] = None
    full_name: str
    department: str
    certificate_type: str
    is_created: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)