from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import User

FORBIDDEN_USERNAMES = [
    'me',
]


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
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
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        max_length=254,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
