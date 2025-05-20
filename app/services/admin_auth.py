# FastAPI
from sqlalchemy.orm.session import Session
import datetime
from jose import jwt, JWTError
from pydantic import ValidationError
from schemas.admin_auth_schema import AdminSignup, AdminSignIn, AdminOut, Token
from core.security import hash_password, verify_password
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from database import get_db
from models import models
from fastapi.security.oauth2 import OAuth2PasswordBearer


oauth2_schema = OAuth2PasswordBearer(tokenUrl='admin_auth/api/admin/auth/login')


def get_current_admin(token: str = Depends(oauth2_schema)):
    try:
        current_admin = AdminAuthService.verify_token(token)
        return current_admin
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=str(err))

class AdminAuthService:
    @classmethod
    def verify_token(cls, token: str):
        try:
            exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate credentials",
                headers={
                    "WWW-Authenticated": 'Bearer'
                }
            )
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))
        try:
            payload = jwt.decode(
                token,
                "secret",
                algorithms=["HS256"]
            )
        except JWTError:
            raise exception

        try:
            admin_data = payload.get('admin')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))

        try:
            admin = AdminOut.parse_obj(admin_data)
        except ValidationError:
            raise exception

        return admin

    @classmethod
    def create_token(cls, admin):
        try:
            admin_data = AdminOut.from_orm(admin)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))

        try:
            now = datetime.datetime.utcnow()
            payload = {
                "exp": now + datetime.timedelta(minutes=43000),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
                "admin": admin_data.dict()
            }
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))

        try:
            token = jwt.encode(payload, "secret", algorithm="HS256")
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
        try:
            access_token = Token(access_token=token)
            return access_token
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def admin_signup(self, adminsignupdata:AdminSignup):
        first_name = adminsignupdata.first_name
        last_name = adminsignupdata.last_name
        email = adminsignupdata.email
        password = hash_password(adminsignupdata.password)
        admin = models.Admin(first_name = first_name, last_name = last_name, email = email, password = password)
        self.session.add(admin)
        self.session.commit()
        return "Ok"

    def admin_login(self, adminlogindata: AdminSignIn):
        email = adminlogindata.email
        password = adminlogindata.password
        admin = self.session.query(models.Admin).filter_by(email = email).first()
        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Admin not found")

        admin = admin.__dict__
        if not verify_password(password, admin.get("password")):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

        return AdminAuthService.create_token({"admin_id": admin.get("admin_id")})







