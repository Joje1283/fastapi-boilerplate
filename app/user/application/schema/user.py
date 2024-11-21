from pydantic import BaseModel


class RegisterUserCommand(BaseModel):
    email: str
    password: str

    class Profile(BaseModel):
        name: str
        age: int
        phone: str

    profile: Profile | None


class LoginQuery(BaseModel):
    email: str
    password: str
