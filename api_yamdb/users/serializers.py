from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import service
from .models import User


class RegistrationSerializer(serializers.Serializer):
    """Сериализация регистрации пользователя и создания нового."""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)

    def validate(self, data):
        """
        Когда email ИЛИ username занят, показать ошибку,
        когда email И username - это один юзер, делегируем решение вьюхе.
        """
        email = data.get('email')
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError('username не может быть me')

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).first()
        if user is None or (user.email == email and user.username == username):
            return data
        raise serializers.ValidationError('Проверьте внимательно '
                                          'email и username')

    def create(self, validated_data):
        code = service.generate_code()
        validated_data['confirmation_code'] = code['hash']
        return User.objects.create_user(**validated_data)


class GetTokenSerializer(serializers.Serializer):
    """Если получили корректный код, выдать токен и уничтожить."""
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=32)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        confirmation_code = service.get_hash(confirmation_code)
        user = get_object_or_404(User, username=username, )
        if confirmation_code and user.confirmation_code == confirmation_code:
            data['token'] = user.token
            user.remove_confirmation_code()
            return data
        raise serializers.ValidationError('Укажите корректный '
                                          'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=2000, required=False)
    role = serializers.ChoiceField(choices=User.ROLE, required=False)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate(self, data):
        """Тут проверим, что email и username свободны для регистрации."""
        email = data.get('email')
        username = data.get('username')
        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exists()
        if user:
            raise serializers.ValidationError('Email или username заняты')
        return data
