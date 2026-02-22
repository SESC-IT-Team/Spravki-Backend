from src.rabbitmq.publisher import CertificateRabbitmqPublisher
from src.schemas.order_shema import CertificateRequest


class OrderService:
    async def create_certificate(self, data: CertificateRequest, info):
        # Сервис отрисовки
        body = {}
        await CertificateRabbitmqPublisher.send_messages(body, certificate_type='aaa')
        return data.type, info

def get_order_service():
    return OrderService