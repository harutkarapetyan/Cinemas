# FastAPI
from sqlalchemy.orm.session import Session
import datetime
from jose import jwt, JWTError
from pydantic import ValidationError
from schemas.user_auth_schema import UserSignup, UserSignIn, UserOut, Token
from core.security import hash_password, verify_password
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from database import get_db
from models import models
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/user_auth/login')


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        current_user = UserAuthService.verify_token(token)
        return current_user
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=str(err))

class UserAuthService:
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
            user_data = payload.get('user')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))

        try:
            user = UserOut.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def create_token(cls, user):
        try:
            user_data = UserOut.from_orm(user)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(err))

        try:
            now = datetime.datetime.utcnow()
            payload = {
                "exp": now + datetime.timedelta(minutes=43000),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
                "user": user_data.dict()
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

    def user_signup(self, usersignupdata:UserSignup):
        first_name = usersignupdata.first_name
        last_name = usersignupdata.last_name
        email = usersignupdata.email
        password = hash_password(usersignupdata.password)
        user = models.User(first_name = first_name, last_name = last_name, email = email, password = password)
        self.session.add(user)
        self.session.commit()
        return "Registration was successful."

    def user_login(self, userlogindata: UserSignIn):
        email = userlogindata.email
        password = userlogindata.password
        user = self.session.query(models.User).filter_by(email = email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

        user = user.__dict__
        if not verify_password(password, user.get("password")):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

        return UserAuthService.create_token({"user_id": user.get("user_id")})







