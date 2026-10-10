from api.exceptions import ResourceNotFoundException
from api.models import UserModel
from api.repositories.note_repository import UserRepository
from api.utils import SecurityUtils
from api.validators.user_validators import (
    UserCreateValidator,
    UserSetPasswordValidator,
    UserUpdateValidator,
)


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def list(self) -> list[UserModel]:
        return self.repository.get_users()

    def show(self, user_id: int) -> UserModel:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return user

    def create(self, user_data: UserCreateValidator) -> UserModel:
        return self.repository.create_note({
            "email": user_data.email,
            "password": SecurityUtils.hash_password(user_data.password)
        })

    def update(self, user_id: int, user_data: UserUpdateValidator) -> UserModel:
        user = self.repository.update_user(user_id, {
            "email": user_data.email,
            "is_active": user_data.is_active,
        })
        if not user:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return user

    def change_password(self, user_id: int, password_data: UserSetPasswordValidator) -> UserModel:
        note = self.repository.change_user_password(user_id, password_data.password)
        if not note:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return note

    def change_status(self, user_id: int, is_active: bool) -> UserModel:
        note = self.repository.change_user_status(user_id, is_active)
        if not note:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return note

    def change_admin(self, user_id: int, is_admin: bool) -> UserModel:
        note = self.repository.change_user_admin(user_id, is_admin)
        if not note:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return note

    def delete(self, user_id: int) -> bool:
        was_deleted = self.repository.delete_user(user_id)
        if not was_deleted:
            raise ResourceNotFoundException(resource_name="User", resource_id=user_id)
        return True
