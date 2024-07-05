from django.contrib import admin

from user.models import User
from common.admin import BaseAbstractModelAdmin


@admin.register(User)
class UserAdmin(BaseAbstractModelAdmin):
    """User model admin"""
    list_display = ('uid', 'username', 'first_name', 'last_name', 'email', 'is_active')
    search_fields = ('uid', 'username', 'email')
    readonly_fields = ('last_login', 'date_joined')
