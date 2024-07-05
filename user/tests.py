import pytest

from user.models import User
from user.v1.serializers import UserSerializer


@pytest.mark.django_db
def test_register_user(api_client, api_base_url):
    new_user = {
        "username": "hermoine",
        "email": "hermoine@example.com",
        "password": "hermoine_password",
        "first_name": "Hermoine",
        "last_name": "Granger"
    }

    response = api_client.post(
        f'{api_base_url}user/register/',
        data=new_user,
    )

    users = User.objects.all()
    expected_data = UserSerializer(users, many=True).data

    assert response.status_code == 201
    assert response.data.get('username') == expected_data[0].get('username')
    assert response.data.get('email') == expected_data[0].get('email')


@pytest.mark.django_db
def test_get_jwt_token(api_client, api_base_url, user_data):
    response = api_client.post(
        f'{api_base_url}user/jwt/token/',
        data=user_data,
    )

    assert response.status_code == 200
    assert response.data.get('access')
