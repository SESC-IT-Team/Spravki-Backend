from pyexpat.errors import messages

from src.rabbitmq.publisher import CertificateRabbitmqPublisher
from src.rabbitmq.tasks.CertificateSchema import AbstractCertificateSchema
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema
from src.rabbitmq.tasks.impl.SocialFoundationCertificate import SocialFoundationCertificate
from src.rabbitmq.tasks.impl.SocialFoundationCertificateSchema import SocialFoundationCertificateSchema
from src.schemas.order_shema import CertificateRequest


class OrderService:
    async def create_certificate(self, headers: HeadersSchema):
        # Сервис отрисовки
        message = {
        "fio": "Пушкинов Александр Сергеевич",
        "birth_date": "06.06.1799",
        "class": "8А",
        "start_date": "01.09.2022",
        "certificate_date": "16.09.2022",
        "certificate_number": "1",
        "end_date": "30.06.2023",
        "order_date": "27.06.2022",
        "order_number": "444/05",
        "vacations": [
            {"start": "30.10.2022", "end": "06.11.2022"},
            {"start": "30.12.2022", "end": "08.01.2023"},
            {"start": "19.03.2023", "end": "30.03.2023"}
        ],
        "academic_director": "М. С. Рябченков"
    }
        obj = CertificateRabbitmqPublisher()


        await obj.send_order_messages(messages=[SocialFoundationCertificateSchema.model_validate(message)], certificate_type=headers.certificate_type)

def get_order_service():
    return OrderService