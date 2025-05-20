from fastapi import APIRouter, Depends
from schemas.user_auth_schema import UserSignup, UserSignIn
from services.user_auth import UserAuthService

user_auth_router = APIRouter(prefix="/api/user/auth", tags=["User Auth"])

@user_auth_router.post("/signup")
def user_signup(usersignupdata: UserSignup, auth_service = Depends(UserAuthService)):
    return auth_service.user_signup(usersignupdata)

@user_auth_router.post("/login")
def user_signup(userlogindata: UserSignIn, auth_service = Depends(UserAuthService)):
    return auth_service.user_login(userlogindata)
