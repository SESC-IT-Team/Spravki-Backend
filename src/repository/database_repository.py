from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.models.order_model import CertificateOrder
from src.rabbitmq.tasks.HeadersSchema import CertificateTypes


class database_repository:
    async def create_order(self, session: AsyncSession, full_name: str, certificate_type: CertificateTypes):
        order = CertificateOrder(full_name=full_name, certificate_type=certificate_type.value)
        session.add(order)



    async def get_orders(self, session: AsyncSession):
        result = await session.execute(select(CertificateOrder))
        return result.scalars().all()

    async def get_false_orders(self, session: AsyncSession):
        items = select(CertificateOrder).where(CertificateOrder.is_created == False)
        result = await session.execute(items)
        orders = result.scalars().all()
        return orders


