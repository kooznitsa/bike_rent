from django.contrib import admin

from rent.models import Rent
from common.admin import BaseAbstractModelAdmin


@admin.register(Rent)
class RentAdmin(BaseAbstractModelAdmin):
    """Bike model admin"""
    list_display = ('uid', 'user', 'bike', 'status', 'start_at', 'finish_at', 'rent_hours', 'total_rent')
    search_fields = ('bike', 'status')
