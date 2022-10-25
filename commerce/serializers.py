from rest_framework import serializers
from commerce.models import Product,Cart,BillingForm

class ProductSerializer(serializers.ModelSerializer) :

    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer) :

    class Meta:
        model = Cart
        fields = '__all__'

class BillingFormSerializer(serializers.ModelSerializer) :
    class Meta:
        model = BillingForm
        fields = '__all__'