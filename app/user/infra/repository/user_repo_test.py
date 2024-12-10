from datetime import datetime
from dataclasses import dataclass
import pytest
from freezegun import freeze_time
from pytest_asyncio import fixture

from app.user.domain.user import User, Profile
from app.user.infra.repository.user_repo import UserRepository


@dataclass
class UserQueryMock:
    id: str
    email: str
    name: str
    age: int
    phone: str
    password: str
    created_at: datetime
    updated_at: datetime


@fixture
async def mock_session(mocker):
    mock_session = mocker.Mock()
    mock_session.exec = mocker.AsyncMock()
    return mock_session


@freeze_time("2024-12-08")
@pytest.mark.asyncio
async def test_find_by_email_user_exists(mocker, mock_session):
    now = datetime.now()
    mock_user = User(
        id="01F9Z3KZ1E4QZJQZJZJZJZJZJZJ",
        email="test@test.com",
        password="password",
        created_at=now,
        updated_at=now,
        profile=Profile(
            name="test",
            age=20,
            phone="1234567890",
        ),
    )
    mock_query_result = UserQueryMock(
        id="01F9Z3KZ1E4QZJQZJZJZJZJZJZJ",
        email="test@test.com",
        name="test",
        age=20,
        phone="1234567890",
        password="password",
        created_at=now,
        updated_at=now,
    )
    mock_session.exec.return_value.one_or_none = mocker.Mock(return_value=mock_query_result)
    user_repository = UserRepository(session=mock_session)
    result = await user_repository.find_by_email(email="test@test.com")
    assert result == mock_user


@freeze_time("2024-12-08")
@pytest.mark.asyncio
async def test_find_by_email_user_does_not_exist(mocker, mock_session):
    mock_session.exec.return_value.one_or_none = mocker.Mock(return_value=None)
    user_repository = UserRepository(session=mock_session)
    result = await user_repository.find_by_email(email="test@test.com")
    assert result is None
