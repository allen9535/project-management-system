from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        datetime_now = timezone.now()

        user = self.model(
            username=username,
            date_joined=datetime_now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True, verbose_name='계정명')
    message = models.TextField(blank=True, null=True, verbose_name='받은 메시지')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    is_staff = models.BooleanField(default=False, verbose_name='스태프 여부')
    is_superuser = models.BooleanField(default=False, verbose_name='슈퍼유저 여부')
    date_joined = models.DateTimeField(auto_now=True, verbose_name='계정 생성일')
    last_login = models.DateTimeField(
        auto_now_add=True,
        verbose_name='마지막 로그인 일시'
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
