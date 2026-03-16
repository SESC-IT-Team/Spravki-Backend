from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.models.order_model import CertificateOrder
from src.rabbitmq.tasks.HeadersSchema import CertificateTypes
from src.schemas.filter_shema import FilterRequest, FilterShema


class database_repository:
    async def create_order(self, session: AsyncSession, full_name: str, certificate_type: CertificateTypes):
        order = CertificateOrder(full_name=full_name, certificate_type=certificate_type.value)
        session.add(order)



    async def get_orders(self, session: AsyncSession, data: FilterRequest):
        if data.filter == FilterShema.date_asc:
            result = await session.execute(select(CertificateOrder).order_by(CertificateOrder.created_at.asc()))
            return result.scalars().all()

        if data.filter == FilterShema.date_desc:
            result = await session.execute(select(CertificateOrder).order_by(CertificateOrder.created_at.desc()))
            return result.scalars().all()

        if data.filter == FilterShema.status_true:
            result = await session.execute(select(CertificateOrder).where(CertificateOrder.is_created == True))
            return result.scalars().all()

        if data.filter == FilterShema.status_false:
            result = await session.execute(select(CertificateOrder).where(CertificateOrder.is_created == False))
            return result.scalars().all()

        if data.filter == FilterShema.none:
            result = await session.execute(select(CertificateOrder))
            return result.scalars().all()


        result = await session.execute(select(CertificateOrder))
        return result.scalars().all()

    async def get_my_orders(self, session: AsyncSession, full_name):
        items = select(CertificateOrder).where(CertificateOrder.full_name == full_name)
        result = await session.execute(items)
        orders = result.scalars().all()
        return orders

    async def get_false_orders(self, session: AsyncSession):
        items = select(CertificateOrder).where(CertificateOrder.is_created == False)
        result = await session.execute(items)
        orders = result.scalars().all()
        return orders


