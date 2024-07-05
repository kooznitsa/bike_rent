from datetime import datetime

from django.db import models

from common.models import BaseAbstractModel


class Rent(BaseAbstractModel):
    """Rent model"""
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('confirmed', 'Confirmed'),
        ('current', 'Current'),
        ('canceled', 'Canceled'),
        ('finished', 'Finished'),
    )

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='User', related_name='rents')
    bike = models.ForeignKey('bike.Bike', on_delete=models.CASCADE, verbose_name='Bike', related_name='rents')
    status = models.CharField('Status', choices=STATUS_CHOICES, max_length=12, default='created')
    start_at = models.DateTimeField('Start time')
    finish_at = models.DateTimeField('End time')

    class Meta:
        verbose_name = 'Rent'
        verbose_name_plural = 'Rents'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['start_at', 'finish_at']),
        ]

    def str_data(self) -> str:
        return f'{self.user} ({self.bike})'

    @property
    def rent_hours(self) -> int:
        if not isinstance(self.start_at, datetime) or not isinstance(self.finish_at, datetime):
            self.start_at = datetime.strptime(self.start_at, r'%Y-%m-%dT%H:%M:%S')
            self.finish_at = datetime.strptime(self.finish_at, r'%Y-%m-%dT%H:%M:%S')
        return (self.finish_at - self.start_at).total_seconds() // 3600

    @property
    def total_rent(self) -> float:
        return self.bike.rent_price * self.rent_hours


class Stats(BaseAbstractModel):
    """Stats model"""
    bike_num = models.IntegerField('Number of bikes', default=0)
    booked_bike_num = models.IntegerField('Number of booked bikes', default=0)
    available_bike_num = models.IntegerField('Number of available bikes', default=0)
    total_rent = models.FloatField('Total rent', default=0.0)

    class Meta:
        verbose_name = 'Stats'
        verbose_name_plural = 'Stats'
        ordering = ('-created_at',)
