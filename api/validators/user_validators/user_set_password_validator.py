from pydantic import model_validator
from typing_extensions import Self

from api.validators.user_validators.user_mixins import (
    PasswordConfirmationMixin,
    PasswordMixin,
)


class UserSetPasswordValidator(PasswordMixin, PasswordConfirmationMixin):
    @model_validator(mode="after")
    def validate_password_confirmation(self) -> Self:
        if self.password != self.password_confirmation:
            raise ValueError("Passwords do not match")
        return self
