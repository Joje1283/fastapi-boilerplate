from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr

from app.user.application.schema.user import RegisterUserCommand
from app.user.application.user_service import UserService
from core.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserBody(BaseModel):
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=4, max_length=32)

    class Profile(BaseModel):
        name: str = Field(min_length=2, max_length=32)
        age: int = Field(ge=18)
        phone: str = Field(max_length=16)

    profile: Profile | None = Field(None, description="User profile")


@router.post("", status_code=201)
@inject
async def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    created_user = await user_service.register_user(
        register_command=RegisterUserCommand(
            email=user.email,
            password=user.password,
            profile=(
                RegisterUserCommand.Profile(name=user.profile.name, age=user.profile.age, phone=user.profile.phone)
                if user.profile
                else None
            ),
        )
    )
    return created_user
