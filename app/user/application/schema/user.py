from pydantic import BaseModel


class RegisterUserCommand(BaseModel):
    email: str
    password: str
    name: str
    age: int
    phone: str


class LoginQuery(BaseModel):
    email: str
    password: str
