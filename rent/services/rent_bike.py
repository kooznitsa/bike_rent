from datetime import datetime

from bike.models import Bike
from rent.models import Rent
from user.models import User


def rent_bike(user_id: str, bike_id: str, start_at: datetime, finish_at: datetime) -> Rent | dict:
    try:
        user = User.objects.get(uid=user_id)
        bike = Bike.objects.get(uid=bike_id)
    except Exception as e:
        return {'error': f'No user or bike found: {e}'}

    active_rents = Rent.objects.filter(status__in=['created', 'confirmed', 'current'])

    # If active rent for user in given dates
    if active_rents.filter(user=user, start_at__gte=start_at, finish_at__lte=finish_at):
        return {'error': f'Dates {start_at} - {finish_at} are already booked by this user'}

    # If bike booked for given dates
    if active_rents.filter(bike=bike, start_at__gte=start_at, finish_at__lte=finish_at):
        return {'error': f'Bike uid={bike_id} is already booked for dates {start_at} - {finish_at}'}

    else:
        return Rent(
            user=user,
            bike=bike,
            start_at=start_at,
            finish_at=finish_at,
        )
