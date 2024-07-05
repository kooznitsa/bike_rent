from django.contrib import admin

from bike.models import Bike
from common.admin import BaseAbstractModelAdmin


@admin.register(Bike)
class BikeAdmin(BaseAbstractModelAdmin):
    """Bike model admin"""
    list_display = ('uid', 'bike_model', 'rent_price')
    search_fields = ('uid', 'bike_model')
