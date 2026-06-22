from uuid import UUID

from pydantic import BaseModel


class DownloadSchema(BaseModel):
    order_id: UUID
