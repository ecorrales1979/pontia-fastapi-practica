from pydantic import EmailStr

from .user_mixins import EmailMixin, IsActiveMixin


class UserUpdateValidator(EmailMixin, IsActiveMixin):
    email: EmailStr | None = None
    is_active: bool | None = None
