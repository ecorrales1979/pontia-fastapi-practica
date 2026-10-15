from .user_mixins import EmailMixin, UsernameMixin
from .user_set_password_validator import UserSetPasswordValidator


class UserCreateValidator(EmailMixin, UsernameMixin, UserSetPasswordValidator):
    pass
