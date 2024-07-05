from django.db import models

from common.models import BaseAbstractModel


class Bike(BaseAbstractModel):
    bike_model = models.CharField('Bike model', max_length=140)
    rent_price = models.FloatField('Rent price', default=0)

    class Meta:
        verbose_name = 'Bike'
        verbose_name_plural = 'Bikes'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['bike_model']),
        ]
