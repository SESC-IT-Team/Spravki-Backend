import json
from pathlib import Path

from sesc_auth_sdk.schemas.user import UserSchema
from datetime import datetime

from src.models.order_model import CertificateOrder
from src.schemas.HeadersSchema import HeadersSchema, CertificateTypes
from sesc_auth_sdk.enums.departments import Department
from src.services.user_service import UserService


class DataService:
    BASE_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates"

    TEMPLATE_MAP = {
        CertificateTypes.SocialFoundation: "SocialFoundaton",
        CertificateTypes.Standard: "Std",
        CertificateTypes.MilitaryRegistration: "Army",
        CertificateTypes.Tax: "TaxFoundation",
    }

    def get_full_name(self, user: UserSchema):
        full_name = user.full_name
        return full_name

    def get_birth_date(self, user: UserSchema):
        birth_date = user.birthday
        return birth_date

    def get_class(self, user: UserSchema):
        class_name = user.class_name
        return class_name

    def get_start_date(self):
        year = datetime.now().year
        return f"01.09.{year}"

    def get_end_date(self):
        year = datetime.now().year
        return f"30.06.{year}"

    def get_certificate_date(self, order: CertificateOrder):
        return order.created_at.strftime("%d.%m.%Y")


    def get_certificate_number(self, order: CertificateOrder):
        number = order.number
        return number



    def get_department(self, headers: HeadersSchema):
        certificate_type = headers.certificate_type

        if (
            certificate_type == CertificateTypes.SocialFoundation
            or certificate_type == CertificateTypes.Standard
            or certificate_type == CertificateTypes.Tax
            or certificate_type == CertificateTypes.MilitaryRegistration
        ):
            return str("educational_department")

        elif (
            certificate_type == CertificateTypes.Certificate
            or certificate_type == CertificateTypes.ExtraditionDocuments
        ):
            return str("competitive_selection_department")

        elif certificate_type == CertificateTypes.Hostel:
            return str("dormitory")

    def get_template_data(self, headers: HeadersSchema, data: UserSchema, order: CertificateOrder) -> dict:
        certificate_type = headers.certificate_type

        template_folder = self.TEMPLATE_MAP.get(certificate_type)

        if not template_folder:
            raise ValueError(f"Шаблон для типа {certificate_type} не найден")

        template_path = self.BASE_TEMPLATE_PATH / template_folder / ".json"

        with open(template_path, "r", encoding="utf-8") as file:
            template_data = json.load(file)

        # Заполняем ТОЛЬКО динамические поля
        replacements = {
            "fio": self.get_full_name(user=data),
            "birth_date": self.get_birth_date(user=data),
            "class": self.get_class(user=data),
            "start_date": self.get_start_date(),
            "end_date": self.get_end_date(),
            "certificate_date": self.get_certificate_date(order=order),  # TODO
            "certificate_number": self.get_certificate_number(order=order),  # TODO
        }

        for key, value in replacements.items():
            if key in template_data:
                template_data[key] = value

        return template_data

    def get_template_html(self, headers: HeadersSchema) -> str:
        certificate_type = headers.certificate_type

        template_folder = self.TEMPLATE_MAP.get(certificate_type)

        if not template_folder:
            raise ValueError(f"HTML шаблон для типа {certificate_type} не найден")

        html_path = self.BASE_TEMPLATE_PATH / template_folder / ".html"

        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        return html_content

