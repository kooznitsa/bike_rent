from bike.v1.views import BikeViewSet

from common.routers import CustomRouter

router = CustomRouter()
router.register('', BikeViewSet, 'bike', ('list',))

urlpatterns = router.urls
