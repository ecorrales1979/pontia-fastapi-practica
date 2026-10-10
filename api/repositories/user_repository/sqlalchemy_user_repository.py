from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.exceptions import DatabaseException
from api.models import UserModel
from api.schemas import UserCreateData, UserUpdateData


class SQLAlchemyUserRepository:

    def __init__(self, session: Session):
        self._db = session

    def get_users(self) -> list[UserModel]:
        try:
            return self._db.query(UserModel).all()
        except SQLAlchemyError as exc:
            raise DatabaseException("Failed to list users", exc) from exc

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        try:
            return self._db.query(UserModel).filter(UserModel.id == user_id).first()
        except SQLAlchemyError as exc:
            raise DatabaseException("Failed to get user by id", exc) from exc

    def create_user(self, user_data: UserCreateData) -> UserModel:
        try:
            new_user = UserModel(**user_data)
            self._db.add(new_user)
            self._db.commit()
            self._db.refresh(new_user)
            return new_user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to create user", exc) from exc

    def update_user(self, user_id: int, user_data: UserUpdateData) -> UserModel | None:
        try:
            user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None
            for key, value in user_data.items():
                setattr(user, key, value)
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to update user", exc) from exc

    def change_user_password(self, user_id: int, new_password: str) -> UserModel | None:
        try:
            user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None
            user.password = new_password
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to change user password", exc) from exc

    def change_user_status(self, user_id: int, is_active: bool) -> UserModel | None:
        try:
            user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None
            user.is_active = is_active
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to change user status", exc) from exc

    def change_user_admin(self, user_id: int, is_admin: bool) -> UserModel | None:
        try:
            user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None
            user.is_admin = is_admin
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to set admin value", exc) from exc

    def delete_user(self, user_id: int) -> bool:
        try:
            user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return False
            self._db.delete(user)
            self._db.commit()
            return True
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to delete user", exc) from exc
