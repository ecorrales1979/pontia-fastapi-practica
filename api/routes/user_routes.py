from fastapi import APIRouter, status

from api.services import UserService
from api.validators.user_validators import (
    UserCreateValidator,
    UserSetActiveValidator,
    UserSetAdminValidator,
    UserUpdateValidator,
)

router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()

@router.get("/")
def list_users():
    return service.list()

@router.get("/{user_id}")
def show_user(user_id: int):
    return service.show(user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateValidator):
    return service.create(payload)

@router.put("/{user_id}")
def update_user(user_id: int, payload: UserUpdateValidator):
    return service.update(user_id, payload)

@router.patch("/{user_id}/status")
def change_user_status(user_id: int, payload: UserSetActiveValidator):
    return service.change_status(user_id=user_id, is_done=payload.is_done)

@router.patch("/{user_id}/set_admin")
def change_user_admin(user_id: int, payload: UserSetAdminValidator):
    return service.change_status(user_id=user_id, is_done=payload.is_done)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    return service.delete(user_id)
