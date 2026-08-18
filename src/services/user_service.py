from aiostream.stream import throw
from fastapi import HTTPException
from pydantic import TypeAdapter, ValidationError
from sesc_auth_sdk.schemas.user import User
from sesc_auth_sdk.enums import role
from starlette import status
import requests
from schemas.HeadersSchema import HeadersSchema, CertificateTypes


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
        if role.Role.student in User.roles:
            return user

        elif role.Role.parent in User.roles:
            res = requests.get("/api/v1/users/me/children").json()
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


async def get_user_service():
    return UserService()