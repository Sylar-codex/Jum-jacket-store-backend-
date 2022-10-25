from rest_framework import routers
from .api import ProductViewSet,CartViewSet,BillingFormViewSet

router = routers.DefaultRouter()
router.register('api/products', ProductViewSet)
router.register('api/carts', CartViewSet,'carts')
router.register('api/billingform', BillingFormViewSet)


urlpatterns = router.urls