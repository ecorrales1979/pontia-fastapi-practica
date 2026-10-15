from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(
            ...,
            min_length=1,
            description="Email must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)


class UsernameMixin(BaseModel):
    username: str = Field(
            ...,
            min_length=1,
            description="Username must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)


class PasswordMixin(BaseModel):
    password: str = Field(
            ...,
            min_length=8,
            description="Password must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)


class PasswordConfirmationMixin(BaseModel):
    password_confirmation: str = Field(
            ...,
            min_length=8,
            description="Password must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)


class IsActiveMixin(BaseModel):
    is_active: bool = Field(
        False,
        description="Indicates whether the user is active"
    )

class IsAdminMixin(BaseModel):
    is_admin: bool = Field(
        False,
        description="Indicates whether the user is an admin"
    )
