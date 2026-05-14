from enum import Enum

from pydantic import BaseModel


class CertificateTypes(Enum):
    SocialFoundation = "SocialFoundation"
    Standard = "Standard"
    MilitaryRegistration = "MilitaryRegistration"
    Tax = "Tax"
    Certificate = "Certificate"
    ExtraditionDocuments = "ExtraditionDocuments"
    Hostel = "Hostel"

class HeadersSchema(BaseModel):
    certificate_type: CertificateTypes

