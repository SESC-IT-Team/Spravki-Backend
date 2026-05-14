from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.db.database import get_session
from src.models.order_model import CertificateOrder
from src.schemas.HeadersSchema import CertificateTypes
from src.schemas.department_shema import DepartmentRequest
from src.schemas.filter_shema import FilterRequest, FilterShema
from src.schemas.order_shema import OrderShema


class DatabaseRepository:


    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order: CertificateOrder):
        self.session.add(order)
        await self.session.commit()  # коммитим здесь
        await self.session.refresh(order)
        return order




    async def get_orders(self, data: FilterRequest, department: DepartmentRequest) -> list[OrderShema]:
        user_department = department.department.value

        if data.filter == FilterShema.date_asc:
            result = await self.session.execute(select(CertificateOrder).where(CertificateOrder.department == user_department).order_by(CertificateOrder.created_at.asc()))
            orders = result.scalars().all()
            return [OrderShema.model_validate(order) for order in orders]

        if data.filter == FilterShema.date_desc:
            result = await self.session.execute(select(CertificateOrder).where(CertificateOrder.department == user_department).order_by(CertificateOrder.created_at.desc()))
            orders = result.scalars().all()
            return [OrderShema.model_validate(order) for order in orders]

        if data.filter == FilterShema.status_true:
            result = await self.session.execute(select(CertificateOrder).where(CertificateOrder.is_created == True and CertificateOrder.department == user_department))
            orders = result.scalars().all()
            return [OrderShema.model_validate(order) for order in orders]

        if data.filter == FilterShema.status_false:
            result = await self.session.execute(select(CertificateOrder).where(CertificateOrder.is_created == False and CertificateOrder.department == user_department))
            orders = result.scalars().all()
            return [OrderShema.model_validate(order) for order in orders]

        if data.filter == FilterShema.none:
            result = await self.session.execute(select(CertificateOrder).where(CertificateOrder.department == user_department))
            orders = result.scalars().all()
            return [OrderShema.model_validate(order) for order in orders]


        result = await self.session.execute(select(CertificateOrder))
        return result.scalars().all()

    async def get_my_orders(self, full_name: str, department: DepartmentRequest) -> list[OrderShema]:
        c_department = department.department.value
        items = select(CertificateOrder).where(
            (CertificateOrder.full_name == full_name) &
            (CertificateOrder.department == c_department)
        )
        result = await self.session.execute(items)
        orders = result.scalars().all()
        return [OrderShema.model_validate(order) for order in orders]

    async def get_false_orders(self, department: DepartmentRequest):
        user_department = department.department.value
        items = select(CertificateOrder).where(
            (CertificateOrder.is_created == False) &
            (CertificateOrder.department == user_department)
        )
        result = await self.session.execute(items)
        orders = result.scalars().all()
        for order in orders:
            order.is_created = True
        await self.session.commit()

    async def set_link(self, number: int, link: str):
        stmt = (
            update(CertificateOrder)
            .where(CertificateOrder.number == number)
            .values(link=link)
        )

        await self.session.execute(stmt)
        await self.session.commit()



async def get_base_repository():
    session = await get_session()
    return DatabaseRepository(session=session)


