from enum import Enum
from pydantic import BaseModel


class CertificateType(str, Enum):
    standard = "standard"
    military = "military"
    tax_service = "tax"
    social_fund = "social"

class CertificateRequest(BaseModel):
    type: CertificateType