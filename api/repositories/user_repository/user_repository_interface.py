from typing import Protocol

from api.models import UserModel
from api.schemas import UserCreateData, UserUpdateData


class UserRepositoryInterface(Protocol):
    def get_users(self) -> list[UserModel]:
        ...

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        ...

    def create_user(self, user_data: UserCreateData) -> UserModel:
        ...

    def update_user(self, user_id: int, user_data: UserUpdateData) -> UserModel | None:
        ...

    def change_user_password(self, user_id: int, new_password: str) -> UserModel | None:
        ...

    def change_user_status(self, user_id: int, is_active: bool) -> UserModel | None:
        ...

    def change_user_admin(self, user_id: int, is_admin: bool) -> UserModel | None:
        ...

    def delete_user(self, user_id: int) -> bool:
        ...
