from uuid import UUID, uuid4


from sqlalchemy import String, DateTime, func, Integer, Boolean, Sequence
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class CertificateOrder(Base):
    __tablename__ = "certificate_actions"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(default=uuid4)
    number: Mapped[int] = mapped_column(Integer, Sequence('document_number_seq'),  nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    department: Mapped[str] = mapped_column(String, nullable=False)
    certificate_type: Mapped[str] = mapped_column(String, nullable=False)
    is_created: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
