from datetime import datetime
import pytest

from app.user.application.schema.user import RegisterUserCommand
from app.user.application.user_service import UserCommandService

from app.user.domain.user import User, Profile
from app.user.interface.controllers import user_controller
from app.user.interface.controllers.schema.user import CreateUserBody
from app.user.interface.controllers.schema.user import Profile as ProfileBody


@pytest.fixture
async def user_interface_dependencies(mocker):
    user_command_service_mock = mocker.Mock(spec=UserCommandService)
    user_mock = User(
        id="TEST_ID",
        email="test@test.com",
        profile=Profile(name="test", age=20, phone="1234567890"),
        password="password",
        created_at=datetime(2024, 12, 8),
        updated_at=datetime(2024, 12, 8),
    )

    return user_command_service_mock, user_mock


@pytest.mark.asyncio
async def test_create_user(user_interface_dependencies):
    (user_command_service_mock, user_mock) = await user_interface_dependencies
    user_command_service_mock.register_user.return_value = user_mock
    await user_controller.create_user(
        body=CreateUserBody(
            email="test@test.com",
            password="password",
            profile=ProfileBody(name="test", age=20, phone="1234567890"),
        ),
        user_service=user_command_service_mock,
    )

    user_command_service_mock.register_user.assert_called_once_with(
        register_command=RegisterUserCommand(
            email="test@test.com",
            password="password",
            profile=(RegisterUserCommand.Profile(name="test", age=20, phone="1234567890")),
        )
    )
