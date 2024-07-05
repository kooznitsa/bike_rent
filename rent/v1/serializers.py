from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rent.models import Rent, Stats
from user.models import User


class UuidRelatedField(SlugRelatedField):
    def __init__(self, slug_field=None, **kwargs):
        slug_field = 'uid'
        super().__init__(slug_field, **kwargs)


class RentSerializer(serializers.ModelSerializer):
    user = UuidRelatedField(queryset=User.objects.all())

    class Meta:
        model = Rent
        fields = ('uid', 'user', 'bike', 'status', 'start_at', 'finish_at', 'rent_hours', 'total_rent')


class BookRentSerializer(serializers.ModelSerializer):
    user = UuidRelatedField(queryset=User.objects.all())

    class Meta:
        model = Rent
        fields = ('user', 'bike', 'start_at', 'finish_at')


class ReturnRentSerializer(serializers.ModelSerializer):
    uid = serializers.CharField()

    class Meta:
        model = Rent
        fields = ('uid',)
