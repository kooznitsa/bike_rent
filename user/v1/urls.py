from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from common.routers import CustomRouter
from .views import UserViewSet

router = CustomRouter()
router.register('', UserViewSet, 'user')


urlpatterns = [
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include('drf_registration.urls')),
    *router.urls
]
