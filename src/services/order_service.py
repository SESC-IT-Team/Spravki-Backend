from uuid import UUID

from sesc_auth_sdk.schemas.user import UserSchema
from document_renderer_sdk.client import AsyncDocumentRendererClient
from src.models.order_model import CertificateOrder
from sesc_auth_sdk.enums.departments import Department
from src.schemas.HeadersSchema import HeadersSchema, CertificateTypes
from src.repository.database_repository import DatabaseRepository, get_base_repository
from src.schemas.department_shema import DepartmentRequest
from src.schemas.filter_shema import FilterRequest
from src.schemas.order_shema import OrderShema
from src.services.data_service import DataService


class OrderService:
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository
        self.data = DataService()

    async def create_certificate(self, headers: HeadersSchema, data: UserSchema, order_data: dict):
        order = await self.create_order(headers=headers, data=data)
        template_data = self.data.get_template_data(headers=headers, data=data, order=order, order_data=order_data)
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

        department = Department(self.data.get_department(headers=headers))
        full_name = self.data.get_full_name(user=data)
        certificate_type = headers.certificate_type
        user_id = self.data.get_user_id(user=data)

        order = CertificateOrder(full_name=full_name, department=department.value,
                                 certificate_type=certificate_type.value, user_id=user_id)

          # создаём сессию здесь
        await self.repository.create_order(
            order=order
        )

        return order


    async def get_orders(self, data: FilterRequest, user: UserSchema) -> list[OrderShema]:
        department = user.department
        return await self.repository.get_orders(data=data, department=DepartmentRequest(department=department))


    async def create_document(self, user: UserSchema, order_id: UUID):
        department = user.department
        await self.repository.get_false_orders(department=DepartmentRequest(department=department), order_id=order_id)


    async def get_my_orders(self,department: DepartmentRequest, user: UserSchema) -> list[OrderShema]:
        user_id = self.data.get_user_id(user=user)
        return await self.repository.get_my_orders(user_id=user_id, department=department)







async def get_order_service():
    return OrderService(repository=(await get_base_repository()))