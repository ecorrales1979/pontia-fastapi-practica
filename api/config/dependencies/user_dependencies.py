from typing import Annotated, TypeAlias

from fastapi import Depends

from api.config.database import DBSessionDependency
from api.repositories.user_repository import (
    SQLAlchemyUserRepository,
    UserRepositoryInterface,
)
from api.services.user_service import UserService


def get_user_repository(db: DBSessionDependency) -> UserRepositoryInterface:
    return SQLAlchemyUserRepository(session=db)

UserRepositoryDependency: TypeAlias = Annotated[UserRepositoryInterface, Depends(get_user_repository)]

def get_user_service(repository: UserRepositoryDependency) -> UserService:
    return UserService(repository=repository)
