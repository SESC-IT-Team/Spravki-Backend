from sesc_auth_sdk.schemas.user import UserSchema
from document_renderer_sdk.client import AsyncDocumentRendererClient
from src.models.order_model import CertificateOrder
from src.schemas.HeadersSchema import HeadersSchema, CertificateTypes
from src.repository.database_repository import DatabaseRepository, get_base_repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import async_session
from src.services.data_service import DataService
from src.schemas.department_shema import DepartmentRequest, DepartmentShema
from src.schemas.filter_shema import FilterRequest
from src.schemas.order_shema import OrderShema
from src.services.data_service import DataService


class OrderService:
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository
        self.data = DataService()

    async def create_certificate(self, headers: HeadersSchema, data: UserSchema):
        order = await self.create_order(headers=headers, data=data)
        template_data = self.data.get_template_data(headers=headers, data=data, order=order)
        template = self.data.get_template_html(headers=headers)
        number = str(self.data.get_certificate_number(order=order))
        filename = "справка_" + number + ".pdf"

        await self.render_document(template_data=template_data, template=template, filename=filename, number=number)


    async def render_document(self, template_data: dict, template: str, filename: str, number: str):
        async with AsyncDocumentRendererClient() as client:
            task_id = await client.render_document(
                template_content=template,
                data=template_data,
                filename=filename
            )

            task_id = str(task_id.file_url)
            await self.repository.set_link(number=int(number), link=task_id)



    async def create_order(self, headers: HeadersSchema, data: UserSchema):

        department = DepartmentShema(self.data.get_department(headers=headers))
        full_name = DataService().get_full_name(user=data)
        certificate_type = headers.certificate_type

        order = CertificateOrder(full_name=full_name, department=department.value,
                                 certificate_type=certificate_type.value)

          # создаём сессию здесь
        await self.repository.create_order(
            order=order
        )

        return order


    async def get_orders(self, session: AsyncSession, data: FilterRequest) -> list[OrderShema]:
        department = DepartmentShema.educational
        return await self.repository.get_orders(session=session, data=data, department=DepartmentRequest(department=department))


    async def create_document(self, session: AsyncSession):
        department = DepartmentShema.educational
        orders = await self.repository.get_false_orders(session=session, department=DepartmentRequest(department=department))
        for order in orders:
            # функция генерации документа
            order.is_created = True
        await session.commit()

    async def get_my_orders(self, session: AsyncSession, department: DepartmentRequest, user: UserSchema) -> list[OrderShema]:
        full_name = user.first_name + " " + user.last_name
        return await self.repository.get_my_orders(session=session, full_name=full_name, department=department)







async def get_order_service():
    return OrderService(repository=(await get_base_repository()))