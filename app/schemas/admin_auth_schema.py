from pydantic import BaseModel, EmailStr

class AdminSignup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class AdminSignIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        from_attributes = True

class AdminOut(BaseModel):
    admin_id: int

    class Config:
        from_attributes = True