from src.models.order_model import CertificateOrder
from src.rabbitmq.publisher import CertificateRabbitmqPublisher
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema, CertificateTypes
from src.rabbitmq.tasks.impl.SocialFoundationCertificateSchema import SocialFoundationCertificateSchema
from src.repository.database_repository import database_repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import async_session
from sqlalchemy import select

from src.schemas.filter_shema import FilterRequest


class OrderService:
    async def create_certificate(self, headers: HeadersSchema, data: dict, department: str):
    #     Сервис отрисовки
    #     message = {
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
        obj = CertificateRabbitmqPublisher()


        await obj.send_order_messages(messages=[SocialFoundationCertificateSchema.model_validate(data)], certificate_type=headers.certificate_type, department=department)

    async def create_order(self, certificate_type: CertificateTypes, full_name: str, department: str):
        async with async_session() as session:  # создаём сессию здесь
            await database_repository().create_order(
                session=session,
                full_name=full_name,
                department=department,
                certificate_type=certificate_type

            )
            await session.commit()  # коммитим здесь

    async def get_orders(self, session: AsyncSession, data: FilterRequest, department: str):
        return await database_repository().get_orders(session=session, data=data, department=department)


    async def create_document(self, session: AsyncSession):
        orders = await database_repository().get_false_orders(session=session)
        for order in orders:
            # функция генерации документа
            order.is_created = True
        await session.commit()

    async def get_my_orders(self, session: AsyncSession, department: str):
        return await database_repository().get_my_orders(session=session, full_name="Пушкинов Александр Сергеевич", department=department)


def get_order_service():
    return OrderService()