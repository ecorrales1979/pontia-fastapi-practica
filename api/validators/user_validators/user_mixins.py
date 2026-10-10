from pydantic import BaseModel, EmailStr, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(
            ...,
            min_length=1,
            strip_whitespace=True,
            description="Email must not be empty"
        )

class PasswordMixin(BaseModel):
    password: str = Field(
            ...,
            min_length=8,
            strip_whitespace=True,
            description="Password must not be empty"
        )

class PasswordConfirmationMixin(BaseModel):
    password_confirmation: str = Field(
            ...,
            min_length=8,
            strip_whitespace=True,
            description="Password must not be empty"
        )

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
