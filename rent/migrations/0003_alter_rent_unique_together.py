# Generated by Django 5.0.6 on 2024-07-04 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0002_remove_rent_rent_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rent',
            unique_together=set(),
        ),
    ]
