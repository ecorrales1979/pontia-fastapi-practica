from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from api.config.database import Base
from api.exceptions import DatabaseException
from api.models import UserModel
from api.repositories.user_repository import SQLAlchemyUserRepository


class TestSQLAlchemyUserRepository:

    @pytest.fixture(autouse=True)
    def _setup_database(self):
        """Prepare a clean SQLite database in memory before each test."""
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(bind=engine)
        testing_session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        self.db_session = testing_session_local()
        self.repository = SQLAlchemyUserRepository(session=self.db_session)

        yield

        self.db_session.close()
        Base.metadata.drop_all(bind=engine)

    # -------------------------------------------------------------------------
    # GET USERS
    # -------------------------------------------------------------------------
    def test_get_users_returns_empty_list_when_no_users(self):
        users = self.repository.get_users()
        assert users == []

    def test_get_users_returns_user_list(self):
        user1 = UserModel(username="user1", email="u1@test.com", password="hash1")
        user2 = UserModel(username="user2", email="u2@test.com", password="hash2")
        self.db_session.add_all([user1, user2])
        self.db_session.commit()

        users = self.repository.get_users()

        assert len(users) == 2
        assert users[0].username == "user1"
        assert users[1].username == "user2"

    def test_get_users_raises_database_exception_on_sqlalchemy_error(self):
        mock_session = MagicMock()
        mock_session.query.side_effect = SQLAlchemyError("DB Error")
        repo = SQLAlchemyUserRepository(session=mock_session)

        with pytest.raises(DatabaseException) as exc_info:
            repo.get_users()

        assert "Failed to list users" in str(exc_info.value)

    # -------------------------------------------------------------------------
    # GET USER BY ID
    # -------------------------------------------------------------------------
    def test_get_user_by_id_returns_user_when_exists(self):
        user = UserModel(username="John", email="john@test.com", password="hash")
        self.db_session.add(user)
        self.db_session.commit()

        found_user = self.repository.get_user_by_id(user.id)

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.username == user.username

    def test_get_user_by_id_returns_none_when_not_exists(self):
        found_user = self.repository.get_user_by_id(999)
        assert found_user is None

    # -------------------------------------------------------------------------
    # CREATE USER
    # -------------------------------------------------------------------------
    def test_create_user_persists_and_returns_user(self):
        user_data = {"username": "pedro", "email": "pedro@test.com", "password": "hashed_pass"}

        created_user = self.repository.create_user(user_data)

        assert created_user.id is not None
        assert created_user.username == "pedro"
        assert created_user.email == "pedro@test.com"

    def test_create_user_raises_database_exception_and_rollbacks_on_error(self):
        mock_session = MagicMock()
        mock_session.add.side_effect = SQLAlchemyError("Insert constraint error")
        repo = SQLAlchemyUserRepository(session=mock_session)

        with pytest.raises(DatabaseException) as exc_info:
            repo.create_user({"username": "fail"})

        assert "Failed to create user" in str(exc_info.value)
        mock_session.rollback.assert_called_once()

    # -------------------------------------------------------------------------
    # UPDATE USER
    # -------------------------------------------------------------------------
    def test_update_user_modifies_fields_and_returns_user(self):
        user = UserModel(username="old_name", email="old@test.com", password="hash")
        self.db_session.add(user)
        self.db_session.commit()

        updated_user = self.repository.update_user(user.id, {"username": "new_name"})

        assert updated_user is not None
        assert updated_user.username == "new_name"
        assert updated_user.email == "old@test.com"

    def test_update_user_returns_none_when_user_not_found(self):
        res = self.repository.update_user(999, {"username": "new"})
        assert res is None

    # -------------------------------------------------------------------------
    # CHANGE USER PASSWORD
    # -------------------------------------------------------------------------
    def test_change_user_password_updates_password(self):
        user = UserModel(username="user_pass", email="pass@test.com", password="old_hash")
        self.db_session.add(user)
        self.db_session.commit()

        updated = self.repository.change_user_password(user.id, "new_hash")

        assert updated is not None
        assert updated.password == "new_hash"

    # -------------------------------------------------------------------------
    # CHANGE USER STATUS
    # -------------------------------------------------------------------------
    def test_change_user_status_updates_is_active(self):
        user = UserModel(username="user_active", email="active@test.com", password="hash", is_active=True)
        self.db_session.add(user)
        self.db_session.commit()

        updated = self.repository.change_user_status(user.id, False)

        assert updated is not None
        assert updated.is_active is False

    # -------------------------------------------------------------------------
    # CHANGE USER IS_ADMIN
    # -------------------------------------------------------------------------
    def test_change_user_admin_updates_is_admin(self):
        user = UserModel(username="user_admin", email="admin@test.com", password="hash", is_admin=False)
        self.db_session.add(user)
        self.db_session.commit()

        updated = self.repository.change_user_admin(user.id, True)

        assert updated is not None
        assert updated.is_admin is True

    # -------------------------------------------------------------------------
    # DELETE USER
    # -------------------------------------------------------------------------
    def test_delete_user_removes_user_and_returns_true(self):
        user = UserModel(username="to_delete", email="del@test.com", password="hash")
        self.db_session.add(user)
        self.db_session.commit()

        deleted = self.repository.delete_user(user.id)

        assert deleted is True
        assert self.repository.get_user_by_id(user.id) is None

    def test_delete_user_returns_false_when_user_not_found(self):
        deleted = self.repository.delete_user(999)
        assert deleted is False
