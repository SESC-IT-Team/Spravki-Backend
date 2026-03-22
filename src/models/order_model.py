from sqlalchemy import String, DateTime, func, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class CertificateOrder(Base):
    __tablename__ = "certificate_actions"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    certificate_type = Column(String, nullable=False)
    is_created = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())