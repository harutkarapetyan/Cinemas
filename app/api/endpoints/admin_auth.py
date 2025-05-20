from fastapi import APIRouter, Depends
from schemas.admin_auth_schema import AdminSignup, AdminSignIn
from services.admin_auth import AdminAuthService


admin_auth_router = APIRouter(prefix="/api/admin/auth", tags=["Admin Auth"],)


@admin_auth_router.post("/signup")
def admin_signup(adminsignupdata: AdminSignup, auth_service = Depends(AdminAuthService)):
    return auth_service.admin_signup(adminsignupdata)


@admin_auth_router.post("/login")
def admin_signin(adminlogindata: AdminSignIn, auth_service = Depends(AdminAuthService)):
    return auth_service.admin_login(adminlogindata)
