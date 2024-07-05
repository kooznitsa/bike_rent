import pytest

from bike.models import Bike
from bike.v1.serializers import BikeSerializer


@pytest.mark.django_db
def test_list_bikes(api_client, api_base_url, create_bikes):
    response = api_client.get(f'{api_base_url}bike/')

    bikes = Bike.objects.all()
    expected_data = BikeSerializer(bikes, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data
