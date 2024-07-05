from datetime import datetime, timedelta

import pytz

from bike.models import Bike
from rent.models import Rent, Stats


def collect_stats() -> dict:
    bike_num = Bike.objects.all().count()

    now = datetime.now(tz=pytz.timezone('Europe/Moscow'))

    booked_rents = Rent.objects.filter(
        status__in=('created', 'confirmed', 'current'),
        start_at__lte=now.strftime('%Y-%m-%dT%H:%M:%S'),
        finish_at__gte=(now + timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M:%S'),
    )
    booked_bikes_uids = [i.bike.uid for i in booked_rents]

    available_bike_num = Bike.objects.exclude(uid__in=booked_bikes_uids).count()
    booked_bike_num = bike_num - available_bike_num
    total_rent = sum(i.total_rent for i in booked_rents)

    stats = Stats(
        bike_num=bike_num,
        available_bike_num=available_bike_num,
        booked_bike_num=booked_bike_num,
        total_rent=total_rent,
    ).__dict__

    del stats['_state']

    return stats
