from typing import Type, Optional, Iterable, Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework.request import Request

from common.models import BaseAbstractModel


class BaseAbstractModelAdmin(admin.ModelAdmin):
    add_exclude: Optional[list[str]] = None
    add_fieldsets: Optional[list[tuple]] = None
    is_secure: bool = False
    add_exclude_checked: bool = False
    host: str = ''

    def clear_add_fieldsets(self, iterable: Iterable) -> list or None:
        """Clearing add fieldsets"""
        total_iterable = list(iterable)

        for element in iterable:

            # clearing
            if element in self.add_exclude:
                total_iterable.remove(element)

            # if iterable, enter recursion
            elif isinstance(element, list | tuple):
                if (new_element := self.clear_add_fieldsets(element)) is None:
                    total_iterable.remove(element)
                else:
                    total_iterable[total_iterable.index(element)] = new_element

        if total_iterable:
            return total_iterable

    def get_fieldsets(self, request: HttpRequest, obj: Optional[Type[BaseAbstractModel]] = None) -> list:
        """Hook for specifying fieldsets"""
        fieldsets = list(super().get_fieldsets(request, obj) or [])

        if obj is None:
            if self.add_fieldsets is None:
                self.add_fieldsets = fieldsets

            if self.add_exclude and not self.add_exclude_checked:
                self.add_fieldsets = [
                    (title, {'fields': self.clear_add_fieldsets(kwargs.get('fields', []))})
                    for title, kwargs in self.add_fieldsets if self.clear_add_fieldsets(kwargs.get('fields', []))
                ]
                self.add_exclude_checked = True
            return self.add_fieldsets or fieldsets

        if self.fieldsets and self.technical not in self.fieldsets:
            fieldsets.append(self.technical)
        return fieldsets

    def get_readonly_fields(self, request: HttpRequest, obj: Optional[Type[BaseAbstractModel]] = None) -> list:
        """Hook for specifying custom readonly fields"""
        if obj is None:
            return []

        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        for field in ('pk',):
            if field not in readonly_fields:
                readonly_fields.append(field)
        return readonly_fields

    def get_queryset(self, request: Request) -> QuerySet[Type[BaseAbstractModel]]:
        """Setting is_secure and host"""
        self.is_secure = request.is_secure()
        self.host = request.get_host()
        return super().get_queryset(request)


class BaseAbstractAdminInline(admin.TabularInline):
    """Base abstract admin model for inlines"""

    def has_delete_permission(self, request: Any, obj: Any = None) -> bool:
        return True

    def has_change_permission(self, request: Any, obj: Any = None) -> bool:
        return True

    def has_add_permission(self, request: Any, obj: Any = None) -> bool:
        return True

    extra = 0


class IsActiveAdmin(admin.ModelAdmin):
    """Is active admin model"""
    list_display = ('is_active',)
    list_filter = ('is_active',)
    readonly_fields = ('is_active',)
    fieldset = ('Active', {'fields': ('is_active',)})
