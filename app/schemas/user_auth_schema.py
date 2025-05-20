from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    user_id: int

    class Config:
        from_attributes = True