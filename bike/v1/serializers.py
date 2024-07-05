from rest_framework import serializers

from bike.models import Bike


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('uid', 'bike_model', 'rent_price')
