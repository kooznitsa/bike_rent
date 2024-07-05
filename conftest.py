from django.conf import settings
import environ
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from bike.models import Bike
from user.models import User

env = environ.Env()


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_TEST_HOST'),
        'PORT': env.str('POSTGRES_TEST_PORT'),
        'ATOMIC_REQUESTS': True,
    }


@pytest.fixture
def user_data():
    return {
        "password": "admin_password",
        "username": "admin"
    }


@pytest.fixture
def superuser(user_data):
    superuser = User.objects.create_superuser(**user_data)
    superuser.save()

    return superuser


@pytest.fixture
def api_client(superuser):
    client = APIClient()
    refresh = RefreshToken.for_user(superuser)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def api_base_url():
    return '/v1/'


@pytest.fixture
def create_bikes():
    bikes = [
        {
          "bike_model": "Kopenhagen Classic Ladies",
          "rent_price": 5.0
        },
        {
          "bike_model": "Rolls-Royce Enthusiasts’ Club",
          "rent_price": 7.0
        }
    ]

    items = []

    for b in bikes:
        bike = Bike.objects.create(**b)
        bike.save()
        items.append(bike)

    return items
