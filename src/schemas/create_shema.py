from uuid import UUID

from pydantic import BaseModel


class CreateShema(BaseModel):
    child_id: UUID