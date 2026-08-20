from uuid import UUID

from sesc_auth_sdk.schemas.user import User
from document_renderer_sdk.client import AsyncDocumentRendererClient

from src.schemas.create_shema import CreateShema
from src.services.user_service import UserService
from src.models.order_model import CertificateOrder
from sesc_auth_sdk.enums.department import Department
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
        self.user = UserService()

    async def create_certificate(self, headers: HeadersSchema, data: User, order_data: dict, child_id: CreateShema):
        self.user.check_role(user=data, headers=headers)
        order = await self.create_order(headers=headers, data=data, child_id=child_id)
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



    async def create_order(self, headers: HeadersSchema, data: User, child_id: CreateShema):

        department = Department(self.data.get_department(headers=headers))
        child = self.user.get_child(child_id=child_id)
        full_name = child.full_name
        certificate_type = headers.certificate_type
        user_id = self.data.get_user_id(user=data)
        child_id = child_id

        order = CertificateOrder(full_name=full_name, department=department.value,
                                 certificate_type=certificate_type.value, user_id=user_id, child_id=child_id.child_id)

          # создаём сессию здесь
        await self.repository.create_order(
            order=order
        )

        return order


    async def get_orders(self, data: FilterRequest, user: User, department: DepartmentRequest) -> list[OrderShema]:
        self.user.check_department_role(department=department)
        return await self.repository.get_orders(data=data, department=department)


    async def create_document(self, user: User, order_id: UUID, department: DepartmentRequest):
        self.user.check_department_role(department=department)
        await self.repository.get_false_orders(department=department, order_id=order_id)


    async def get_my_orders(self,department: DepartmentRequest, user: User) -> list[OrderShema]:
        return await self.repository.get_my_orders(user=user, department=department)







async def get_order_service():
    return OrderService(repository=(await get_base_repository()))