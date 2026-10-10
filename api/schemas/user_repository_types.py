from typing import TypedDict


class UserCreateData(TypedDict):
    email: str
    password: str

class UserUpdateData(TypedDict):
    email: str | None = None
    is_active: bool | None = None
