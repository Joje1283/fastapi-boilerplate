from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from core.application.dto.user import RegisterUserCommand, LoginQuery
from core.application.service.user_service import UserCommandService, UserQueryService
from core.user.interface.controllers.schema.user import CreateUserResponse, CreateUserBody, LoginBody
from core.infra.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201, response_model=CreateUserResponse)
@inject
async def create_user(
    body: CreateUserBody,
    user_service: UserCommandService = Depends(Provide[Container.user_command_service]),
):
    created_user = await user_service.register_user(
        register_command=RegisterUserCommand(
            email=body.email,
            password=body.password,
            profile=(
                RegisterUserCommand.Profile(name=body.profile.name, age=body.profile.age, phone=body.profile.phone)
                if body.profile
                else None
            ),
        )
    )
    return created_user


@router.post("/login", status_code=200)
@inject
async def login(
    body: LoginBody,
    user_service: UserQueryService = Depends(Provide[Container.user_query_service]),
):
    return await user_service.login(
        login_query=LoginQuery(
            email=body.email,
            password=body.password,
        )
    )
