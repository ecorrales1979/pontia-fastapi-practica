from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints


class EmailMixin(BaseModel):
    email: Annotated[
        str,
        EmailStr,
        StringConstraints(strip_whitespace=True),
        Field(min_length=1, description="Email must not be empty")
    ]


class UsernameMixin(BaseModel):
    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=1, description="Username must not be empty")
    ]


class PasswordMixin(BaseModel):
    password: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=8, description="Password must not be empty")
    ]


class PasswordConfirmationMixin(BaseModel):
    password_confirmation: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=8, description="Password must not be empty")
    ]


class IsActiveMixin(BaseModel):
    is_active: Annotated[
        bool,
        Field(description="Indicates whether the user is active")
    ]

class IsAdminMixin(BaseModel):
    is_admin: Annotated[
        bool,
        Field(description="Indicates whether the user is an admin")
    ]
