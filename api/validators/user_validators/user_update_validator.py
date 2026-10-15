from pydantic import EmailStr

from .user_mixins import EmailMixin, IsActiveMixin, UsernameMixin


class UserUpdateValidator(EmailMixin, IsActiveMixin, UsernameMixin):
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None
