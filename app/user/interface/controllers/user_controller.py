from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.user.application.schema.user import RegisterUserCommand, LoginQuery
from app.user.application.user_service import UserService
from app.user.interface.controllers.schema.user import CreateUserResponse, CreateUserBody, LoginBody
from core.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201, response_model=CreateUserResponse)
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


@router.post("/login", status_code=200)
@inject
async def login(
    body: LoginBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.login(
        login_query=LoginQuery(
            email=body.email,
            password=body.password,
        )
    )