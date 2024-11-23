from sqlmodel import select
from sqlmodel import and_

from app.user.domain.repository.user_repo import AbcUserRepository
from app.user.domain.user import User as UserEntity
from app.user.infra.model.user import User, Profile
from core.database import session_factory, session


class UserRepository(AbcUserRepository):
    async def save(self, user: UserEntity) -> UserEntity:
        user_model = User(
            id=user.id,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        session.add(user_model)
        await session.flush()
        if user.profile:
            session.add(
                Profile(
                    user_id=user.id,
                    name=user.profile.name,
                    age=user.profile.age,
                    phone=user.profile.phone,
                )
            )
        return user

    async def find_by_email(self, email: str) -> UserEntity | None:
        entries = [
            User.id,
            User.email,
            User.password,
            User.created_at,
            User.updated_at,
            Profile.name,
            Profile.age,
            Profile.phone,
        ]
        query = select(*entries)

        query = query.join(
            Profile,
            and_(User.id == Profile.user_id),
            isouter=True,
        )
        query = query.where(and_(User.email == email))
        async with session_factory() as read_session:
            result = await read_session.exec(query)
            result = result.one_or_none()
            if result:
                return UserEntity(
                    id=result.id,
                    email=result.email,
                    password=result.password,
                    profile=(
                        Profile(
                            name=result.name,
                            age=result.age,
                            phone=result.phone,
                        )
                        if result.name
                        else None
                    ),
                    created_at=result.created_at,
                    updated_at=result.updated_at,
                )

    async def delete(self) -> None:
        pass
