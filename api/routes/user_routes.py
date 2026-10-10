from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.config.dependencies.user_dependencies import get_user_service
from api.services import UserService
from api.validators.user_validators import (
    UserCreateValidator,
    UserSetActiveValidator,
    UserSetAdminValidator,
    UserUpdateValidator,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_user_service)]
)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]

@router.get("/")
def list_users(service: UserServiceDependency):
    return service.list()

@router.get("/{user_id}")
def show_user(
    user_id: int,
    service: UserServiceDependency
):
    return service.show(user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateValidator,
    service: UserServiceDependency
):
    return service.create(payload)

@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdateValidator,
    service: UserServiceDependency
):
    return service.update(user_id, payload)

@router.patch("/{user_id}/status")
def change_user_status(
    user_id: int,
    payload: UserSetActiveValidator,
    service: UserServiceDependency
):
    return service.change_status(user_id=user_id, is_done=payload.is_done)

@router.patch("/{user_id}/set_admin")
def change_user_admin(
    user_id: int,
    payload: UserSetAdminValidator,
    service: UserServiceDependency
):
    return service.change_status(user_id=user_id, is_done=payload.is_done)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserServiceDependency
):
    return service.delete(user_id)
