from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

FORBIDDEN_USERNAMES = (
    'me',
)
MAX_USERNAME_LENGTH = 150
MAX_FIELD_LENGTH = 254


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор создание пользователя."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )
    email = serializers.EmailField(
        max_length=MAX_FIELD_LENGTH,
        required=True
    )

    def validate_username(self, value):
        if value.lower() in FORBIDDEN_USERNAMES:
            raise serializers.ValidationError(
                f'Использовать имя - {value} - запрещено!'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким username — {value} — уже существует!'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким email - {value} - уже существует!'
            )
        return value


class UserReceiveTokenSerializer(serializers.Serializer):
    """Сериализатор получение токена."""
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=MAX_FIELD_LENGTH,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_FIELD_LENGTH,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
