from datetime import datetime, timedelta, timezone
from fastapi import Request
from jose import jwt
from fastapi.responses import RedirectResponse
from src.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


class AuthService:

    def create_token(self, full_name: str, clas: str):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "full_name": full_name,
            "clas": clas,
            "exp": expire
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        response = RedirectResponse(url="/", status_code=302)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True
        )
        return response


    def token_info(self, request: Request):
        token = request.cookies.get("access_token")

        if not token:
            return RedirectResponse(url="/login", status_code=302)


        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("full_name"), payload.get("clas")

        except:
            return RedirectResponse(url="/login", status_code=302)


def get_auth_service() -> AuthService:
    return AuthService()