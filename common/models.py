import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse


class BaseAbstractModel(models.Model):
    """Base abstract model"""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField('Created', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | {self.str_data()}'

    def str_data(self) -> str:
        return self.pk

    @classmethod
    def get_admin_url(cls) -> str:
        """Get relative reference to list"""
        content_type = ContentType.objects.get_for_model(cls)
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist')


class IsActiveManager(models.Manager):
    """Base abstract custom manager"""

    def get_queryset(self) -> QuerySet:
        return QuerySet(model=self.model, using=self._db)

    def active(self) -> QuerySet:
        return self.get_queryset().filter(is_active=True)

    def inactive(self) -> QuerySet:
        return self.get_queryset().filter(is_active=False)


class IsActive(models.Model):
    """Base abstract model with custom manager"""
    is_active = models.BooleanField('Is active', default=True)

    objects = IsActiveManager()

    class Meta:
        abstract = True
