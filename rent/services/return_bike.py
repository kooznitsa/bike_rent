from datetime import datetime

import pytz

import core.settings as settings
from rent.models import Rent


def return_bicycle(rent_id: str) -> Rent | dict:
    try:
        rent = Rent.objects.get(uid=rent_id)

        if rent.status in ('canceled', 'finished'):
            return {'error': 'Rent is already canceled/finished'}

        elif rent.status in ('created', 'confirmed'):
            rent.status = 'canceled'
            rent.save(update_fields=('status',))

        elif rent.status in ('current',):
            rent.status = 'finished'
            rent.save(update_fields=('status',))

        rent.finish_at = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        rent.save(update_fields=('finish_at',))

        return rent

    except Exception as e:
        return {'error': f'No object found: {e}'}
