from .user_mixins import EmailMixin
from .user_set_password_validator import UserSetPasswordValidator


class UserCreateValidator(EmailMixin, UserSetPasswordValidator):
    pass
