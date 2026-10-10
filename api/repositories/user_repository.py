from sqlalchemy.exc import SQLAlchemyError

from api.config.database import SessionLocal
from api.exceptions import DatabaseException
from api.models import UserModel
from api.schemas import UserCreateData, UserUpdateData


class UserRepository:
    def get_users(self) -> list[UserModel]:
        with SessionLocal() as db:
            try:
                return db.query(UserModel).all()
            except SQLAlchemyError as exc:
                raise DatabaseException("Failed to list users", exc) from exc

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        with SessionLocal() as db:
            try:
                return db.query(UserModel).filter(UserModel.id == user_id).first()
            except SQLAlchemyError as exc:
                raise DatabaseException("Failed to get user by id", exc) from exc

    def create_user(self, user_data: UserCreateData) -> UserModel:
        with SessionLocal() as db:
            try:
                new_user = UserModel(**user_data)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to create user", exc) from exc

    def update_user(self, user_id: int, user_data: UserUpdateData) -> UserModel | None:
        with SessionLocal() as db:
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if not user:
                    return None
                for key, value in user_data.items():
                    setattr(user, key, value)
                db.commit()
                db.refresh(user)
                return user
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to update user", exc) from exc

    def change_user_password(self, user_id: int, new_password: str) -> UserModel | None:
        with SessionLocal() as db:
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if not user:
                    return None
                user.password = new_password
                db.commit()
                db.refresh(user)
                return user
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to change user password", exc) from exc

    def change_user_status(self, user_id: int, is_done: bool) -> UserModel | None:
        with SessionLocal() as db:
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if not user:
                    return None
                user.is_done = is_done
                db.commit()
                db.refresh(user)
                return user
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to change user status", exc) from exc

    def change_user_admin(self, user_id: int, is_admin: bool) -> UserModel | None:
        with SessionLocal() as db:
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if not user:
                    return None
                user.is_admin = is_admin
                db.commit()
                db.refresh(user)
                return user
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to set admin value", exc) from exc

    def delete_user(self, user_id: int) -> bool:
        with SessionLocal() as db:
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if not user:
                    return False
                db.delete(user)
                db.commit()
                return True
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to delete user", exc) from exc
