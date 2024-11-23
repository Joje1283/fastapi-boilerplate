from pydantic import BaseModel, EmailStr


class RegisterUserCommand(BaseModel):
    email: EmailStr
    password: str

    class Profile(BaseModel):
        name: str
        age: int
        phone: str

    profile: Profile | None


class LoginQuery(BaseModel):
    email: EmailStr
    password: str
