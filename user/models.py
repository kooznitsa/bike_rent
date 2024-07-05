from typing import Any, Optional
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from common.models import IsActive, IsActiveManager


class CustomUserManager(UserManager, IsActiveManager):
    """Custom user manager"""

    def create_user(self, password: Optional[str] = None, **kwargs: Any) -> 'User':
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password: Optional[str] = None, **kwargs: Any) -> 'User':
        return self.create_user(password, is_staff=True, is_superuser=True, **kwargs)


class User(IsActive, AbstractUser):
    """User model"""
    user_permissions = None

    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField('Username', max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField('Email', default='', blank=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-date_joined',)

    def str_data(self) -> str:
        return f'{self.email}'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
