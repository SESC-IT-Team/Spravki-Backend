from datetime import datetime, timedelta
from fastapi import Request
from jose import jwt
from fastapi.responses import RedirectResponse

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:

    def create_token(self, username: str):
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": username, "exp": expire}

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        response = RedirectResponse(url="/", status_code=302)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True
        )
        return response


    def check_token(self, request: Request):
        token = request.cookies.get("access_token")

        if not token:
            return RedirectResponse(url="/login", status_code=302)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")

        except:
            return RedirectResponse(url="/login", status_code=302)

