from freezegun import freeze_time
import pytest
from ulid import ULID

from app.user.application.schema.user import RegisterUserCommand
from app.user.application.user_service import UserCommandService, UserQueryService
from app.user.domain.user import User, Profile
from core.uow.abstract import AbcUnitOfWork
from utils.hashing import Crypto


@pytest.fixture
async def user_service_dependencies(mocker):
    uow_mock = mocker.Mock(spec=AbcUnitOfWork)
    ulid_mock = mocker.Mock(spec=ULID)
    crypto_mock = mocker.Mock(spec=Crypto)
    uow_mock.user_repo = mocker.AsyncMock()

    # async context manager (UnitOfWork)
    async def aenter():
        return uow_mock

    async def aexit(exc_type, exc_val, exc_tb):
        pass

    uow_mock.__aenter__ = mocker.AsyncMock(side_effect=aenter)
    uow_mock.__aexit__ = mocker.AsyncMock(side_effect=aexit)

    return (
        uow_mock,
        ulid_mock,
        crypto_mock,
    )


@freeze_time("2024-12-08")
@pytest.mark.asyncio
async def test_create_user_success(user_service_dependencies):
    (
        uow_mock,
        ulid_mock,
        crypto_mock,
    ) = await user_service_dependencies
    user_command_service = UserCommandService(crypto=crypto_mock, write_uow=uow_mock, ulid=ulid_mock)

    email = "test@test.com"
    password = "password"
    id = "01F9Z3KZ1E4QZJQZJZJZJZJZJZJ"

    ulid_mock.generate.return_value = id
    uow_mock.user_repo.find_by_email.return_value = None
    uow_mock.user_repo.save.return_value = None
    crypto_mock.encrypt.return_value = password

    user_command = RegisterUserCommand(
        email=email, password=password, profile=RegisterUserCommand.Profile(name="test", age=20, phone="1234567890")
    )
    user = await user_command_service.register_user(user_command)

    assert isinstance(user, User)
    assert user.id == id
    assert user.email == email
    assert user.created_at.year == 2024
    assert user.created_at.day == 8

    user_command_service.uow.user_repo.find_by_email.assert_called_once_with(email=email)
    user_command_service.uow.user_repo.save.assert_called_once_with(
        user=User(
            id=id,
            email=email,
            password=password,
            profile=Profile(name="test", age=20, phone="1234567890"),
            created_at=user.created_at,
            updated_at=user.created_at,
        )
    )
    user_command_service.crypto.encrypt.assert_called_once_with(password)