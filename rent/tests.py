import pytest

from bike.models import Bike
from rent.models import Rent
from rent.services.rent_bike import rent_bike
from rent.services.return_bike import return_bicycle
from user.models import User


def rent_data(user, bike):
    return [
        {
            "user": user,
            "bike": bike,
            "start_at": "2024-07-05T06:31:13",
            "finish_at": "2024-07-06T06:31:13"
        },
        # Rent in other dates
        {
            "user": user,
            "bike": bike,
            "start_at": "2024-07-07T06:31:13",
            "finish_at": "2024-07-08T06:31:13"
        },
        # Rent in the same dates
        {
            "user": user,
            "bike": bike,
            "start_at": "2024-07-05T06:31:13",
            "finish_at": "2024-07-06T06:31:13"
        },
    ]


def create_rents(user, bike):
    for rent in rent_data(user, bike):
        rent = Rent.objects.create(**rent)
        rent.save()


@pytest.mark.django_db
def test_user_rent_history(api_client, api_base_url, create_bikes):
    user = User.objects.first()
    bike = Bike.objects.first()
    create_rents(user, bike)

    response = api_client.get(
        f'{api_base_url}rent/history/',
    )

    rents = Rent.objects.all()

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_bike(api_client, create_bikes):
    user = User.objects.first().uid
    bike = Bike.objects.first().uid
    data, _, _ = rent_data(user, bike)

    booking = rent_bike(*data.values())

    assert isinstance(booking, Rent)


@pytest.mark.django_db
def test_book_bike_error(api_client, create_bikes):
    user = User.objects.first()
    bike = Bike.objects.first()

    rent = Rent.objects.create(
        user=user, bike=bike,
        start_at="2024-07-05T06:31:13", finish_at="2024-07-06T06:31:13",
    )
    rent.save()

    _, _, error_data = rent_data(user.uid, bike.uid)

    booking = rent_bike(*error_data.values())
    assert booking.get('error').endswith('are already booked by this user')


@pytest.mark.django_db
def test_book_bike_endpoint(api_client, api_base_url, create_bikes):
    user = User.objects.first().uid
    bike = Bike.objects.first().uid
    data = rent_data(user, bike)

    response_0 = api_client.post(
        f'{api_base_url}rent/book_bike/',
        data=data[0],
    )

    assert response_0.status_code == 201
    assert response_0.json().get('status') == 'created'

    response_1 = api_client.post(
        f'{api_base_url}rent/book_bike/',
        data=data[1],
    )

    assert response_1.status_code == 201
    assert response_1.json().get('status') == 'created'

    response_2 = api_client.post(
        f'{api_base_url}rent/book_bike/',
        data=data[2],
    )

    assert response_2.status_code == 422
    assert response_2.content.endswith(b'are already booked by this user')


@pytest.mark.django_db
def test_return_bike(api_client, create_bikes):
    user = User.objects.first()
    bike = Bike.objects.first()

    rent = Rent.objects.create(
        user=user, bike=bike,
        start_at="2024-07-05T06:31:13", finish_at="2024-07-06T06:31:13",
    )
    rent.save()

    returned = return_bicycle(rent.uid)

    assert returned.status == 'canceled'


@pytest.mark.django_db
def test_return_bike_endpoint(api_client, api_base_url, create_bikes):
    user = User.objects.first()
    bike = Bike.objects.first()
    create_rents(user, bike)

    data = {
      "uid": Rent.objects.first().uid
    }

    response = api_client.post(
        f'{api_base_url}rent/return_bike/',
        data=data,
    )

    assert response.status_code == 200
    assert response.json().get('status') == 'canceled'
