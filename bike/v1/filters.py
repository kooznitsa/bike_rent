import re

from django.db.models import QuerySet
from django_filters import rest_framework as filters

from bike.models import Bike


class BikeFilter(filters.FilterSet):
    """Bike filter"""
    bike_model = filters.CharFilter(field_name='bike_model', method='filter_model', label='Bike model')

    def filter_model(self, queryset: QuerySet[Bike], name: str, value: str) -> QuerySet[Bike]:
        return queryset.filter(bike_model__in=re.split(r'[;,]', value))

    class Meta:
        model = Bike
        fields = ('bike_model',)
