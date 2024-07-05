from __future__ import absolute_import, unicode_literals
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

from rent.models import Stats
from rent.services.stats import collect_stats

celery_app = Celery('core')
celery_app.conf.enable_utc = False

celery_app.config_from_object(settings, namespace='CELERY')

celery_app.conf.update(
    task_serializer='json',
    accept_content=['application/json'],
    result_serializer='json',
    beat_schedule={
        'collect_statistics': {
            'task': 'core.celery.collect_statistics',
            'schedule': crontab(hour='*/6'),
        },
    },
    task_routes={
        'core.celery.collect_statistics': 'main-queue',
    },
)

celery_app.autodiscover_tasks()


@celery_app.task
def collect_statistics():
    stats = collect_stats()
    Stats.objects.create(**stats)
