from pydantic import BaseModel

class Certificate(BaseModel):
    student_name: str
    _class: str
    contact_number: str
    contact_email: str
    need_grade: bool
    reason: str

class ExtraditionDocuments(BaseModel):
    student_full_name: str
    class_: str
    contact_phone: str
    contact_email: str
    location_for_certificate: str
    need_grade: bool



class HostelShema(BaseModel):
    parent_full_name: str
    student_full_name: str
    reason_for_stay: str
    stay_location: str
    contact_person: str
    leaving_time: str
    returning_time: str