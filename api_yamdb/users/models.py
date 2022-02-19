from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from . import service


class UserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None,
                    confirmation_code=None,
                    role='user',
                    bio='',
                    ):
        if username is None:
            raise TypeError('У юзера должен быть юзернейм.')

        if email is None:
            raise TypeError('У юзера дожен быть адрес email.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            confirmation_code=confirmation_code,
            role=role,
            bio=bio,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = [
        (USER, 'Юзер'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    ]
    username = models.CharField(db_index=True, max_length=150, unique=True,
                                verbose_name='Логин')
    email = models.EmailField(db_index=True, max_length=254, unique=True,
                              verbose_name='Эл.почта')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation_code = models.CharField(db_index=True, max_length=32,
                                         null=True)
    first_name = models.CharField(max_length=150, null=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150, null=True,
                                 verbose_name='Фамилия')
    bio = models.CharField(max_length=2000, null=True, verbose_name='О себе')
    role = models.CharField(max_length=16,
                            choices=ROLE,
                            default=USER,
                            verbose_name='Роль')
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'user_id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def set_confirmation_code(self):
        """Устанавливает код_подтверждения у юзера."""
        code = service.generate_code()
        self.confirmation_code = code['hash']
        self.save()
        return code

    def remove_confirmation_code(self):
        """Удаляет код_подтверждения у юзера."""
        self.confirmation_code = 0
        self.save()

    @property
    def is_admin(self):
        """Дадим юзеру лаконичный bool проверки на админ-права."""
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """Дадим юзеру лаконичный bool проверки на модераторские права."""
        return self.role == self.MODERATOR
