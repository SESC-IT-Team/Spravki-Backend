from enum import Enum

from pydantic import BaseModel


class CertificateTypes(Enum):
    SocialFoundation = "SocialFoundation"

class HeadersSchema(BaseModel):
    certificate_type: CertificateTypes
