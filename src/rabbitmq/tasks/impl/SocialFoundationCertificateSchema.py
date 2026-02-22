from src.rabbitmq.tasks.CertificateSchema import AbstractCertificateSchema


class SocialFoundationCertificateSchema(AbstractCertificateSchema):
    fio: str
    birth_date: str
    _class: str
    start_date: str
    certificate_date: str
    certificate_number: str
    end_date: str
    order_date: str
    order_number: str
    vacations: list[dict]
    academic_director: str

# {
#     "fio": "Пушкинов Александр Сергеевич",
#     "birth_date": "06.06.1799",
#     "class": "8А",
#     "start_date": "01.09.2022",
#     "certificate_date": "16.09.2022",
#     "certificate_number": "1",
#     "end_date": "30.06.2023",
#     "order_date": "27.06.2022",
#     "order_number": "444/05",
#     "vacations": [
#         {"start": "30.10.2022", "end": "06.11.2022"},
#         {"start": "30.12.2022", "end": "08.01.2023"},
#         {"start": "19.03.2023", "end": "30.03.2023"}
#     ],
#     "academic_director": "М. С. Рябченков"
# }