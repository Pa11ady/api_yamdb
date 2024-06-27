from enum import Enum


class UserRoles(Enum):
    """Обработка ролей."""
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'
    superuser = 'superuser'

    @classmethod
    def choices(cls):
        return tuple((attribute.name, attribute.value) for attribute in cls)
