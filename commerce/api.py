from commerce.models import Product,Cart,BillingForm
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, CartSerializer,BillingFormSerializer
from knox.auth import TokenAuthentication

class ProductViewSet(viewsets.ModelViewSet) :
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet) :
    authentication_classes =(TokenAuthentication,)
    permission_classes = {
        permissions.IsAuthenticated
    }
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.request.user.carts.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BillingFormViewSet(viewsets.ModelViewSet) :
    queryset = BillingForm.objects.all()
    serializer_class = BillingFormSerializer
    