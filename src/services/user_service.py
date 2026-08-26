from uuid import UUID

from aiostream.stream import throw
from fastapi import HTTPException
from pydantic import TypeAdapter, ValidationError
from sesc_auth_sdk.schemas.user import User
from sesc_auth_sdk.enums import role
from starlette import status
import requests

from src.config import settings
from src.schemas.HeadersSchema import HeadersSchema, CertificateTypes
from src.schemas.create_shema import CreateShema
from src.schemas.department_shema import DepartmentRequest


class UserService:
    def __init__(self):
        pass

    def check_role(self, user: User, headers: HeadersSchema):
        if headers.certificate_type in [CertificateTypes.Standard, CertificateTypes.Tax, CertificateTypes.MilitaryRegistration, CertificateTypes.SocialFoundation]:
            if role.Role.student in user.roles:
                return

            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


        elif headers.certificate_type in [CertificateTypes.ExtraditionDocuments, CertificateTypes.Certificate]:
            if role.Role.student in user.roles:
                return

            elif role.Role.parent in user.roles:
                return

            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


        elif headers.certificate_type == CertificateTypes.Hostel:
            if role.Role.parent in user.roles:
                return
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)




    def get_children(self, user: User, headers: HeadersSchema):
        if role.Role.student in user.roles:
            return [user]

        elif role.Role.parent in user.roles:
            res = requests.get(settings.user_service_url + "/v1/users/me/children").json()
            try:
                # 2. Создаем адаптер для списка моделей User
                user_list_adapter = TypeAdapter(list[User])

                # 3. Валидируем массив.
                # На выходе получаем чистый Python-список из объектов User
                validated_users: list[User] = user_list_adapter.validate_python(res)

                if headers.certificate_type == CertificateTypes.Hostel:
                    users: list[User] = []
                    for i in validated_users:
                        if i.lives_in_dormitory:
                            users.append(i)

                    return users
                else:
                    return validated_users



            except ValidationError as e:

                print("Данные не соответствуют модели User:")
                print(e.json(indent=2))






            return res

    def check_department_role(self, department: DepartmentRequest):
        department_name = department.department.value
        res = requests.get(f"/v1/departments/{department_name}/members/me", ).json()
        if res.status_code == 200:
            return
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


    def get_child(self, child_id: CreateShema):
        res = requests.get(settings.user_service_url + f"/v1/users/me/children/{child_id.child_id}").json()
        try:
            # 2. Создаем адаптер для списка моделей User
            user_adapter = TypeAdapter(User)

            # 3. Валидируем массив.
            # На выходе получаем чистый Python-список из объектов User
            validated_user: User = user_adapter.validate_python(res)
            return validated_user




        except ValidationError as e:

            print("Данные не соответствуют модели User:")
            print(e.json(indent=2))

    def get_child_or_me(self, child_id: CreateShema, user: User):
        if user.id == child_id.child_id:
            return user
        return self.get_child(child_id=child_id)


    def get_children_id(self):
        res = requests.get(settings.user_service_url + "/v1/users/me/children").json()
        try:
            # 2. Создаем адаптер для списка моделей User
            user_list_adapter = TypeAdapter(list[User])

            # 3. Валидируем массив.
            # На выходе получаем чистый Python-список из объектов User
            validated_users: list[User] = user_list_adapter.validate_python(res)

            users_id: list[UUID] = []
            for user in validated_users:
                users_id.append(user.id)

            return users_id

        except ValidationError as e:

            print("Данные не соответствуют модели User:")
            print(e.json(indent=2))


async def get_user_service():
    return UserService()