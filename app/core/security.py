from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUETS = 43200
ACCESS_TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_SECRET = "SECRET"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
