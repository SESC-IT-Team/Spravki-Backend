from src.schemas.order_shema import CertificateRequest


class OrderService:
    def create_certificate(self, data: CertificateRequest, info):
        return data.type, info
        # Сервис отрисовки

def get_order_service():
    return OrderService