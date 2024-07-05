from dataclasses import dataclass

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


@dataclass
class JWTService:
    """Service for generating JWT tokens by user"""

    @staticmethod
    def generate_tokens(user: User) -> dict:
        token = TokenObtainPairSerializer.get_token(user)
        return {'access': str(token.access_token), 'refresh': str(token)}

    @staticmethod
    def generate_error() -> dict:
        return {'access': '', 'refresh': ''}
