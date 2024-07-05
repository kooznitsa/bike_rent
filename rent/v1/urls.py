from rent.v1.views import RentViewSet

from common.routers import CustomRouter

router = CustomRouter()
router.register('', RentViewSet, 'book_bike')
router.register('', RentViewSet, 'return_bike')
router.register('', RentViewSet, 'history')

urlpatterns = router.urls
