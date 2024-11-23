from pydantic import BaseModel, EmailStr, Field


class Profile(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    age: int = Field(ge=18)
    phone: str = Field(max_length=16)


class CreateUserBody(BaseModel):
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=4, max_length=32)
    profile: Profile | None = Field(None, description="User profile")


class CreateUserResponse(BaseModel):
    id: str
    email: str
    profile: Profile | None


class LoginBody(BaseModel):
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=4, max_length=32)
