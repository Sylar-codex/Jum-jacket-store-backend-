from wsgiref.validate import validator
from rest_framework import serializers
from django.db.models import Sum 
from .models import Wallet, WalletTransaction
from django.conf import settings
from django.contrib.auth.models import User
import requests


class WalletSerializer(serializers.ModelSerializer) :
    # serializer to validate user waller
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj) :
        bal = WalletTransaction.objects.filter(wallet=obj, status="success").aggregate(Sum('amount'))['amount__sum']
        return bal

    class Meta :
        model = Wallet
        fields = ['id','currency','balance']
    
def is_amount(value) :
    if value <= 0:
        raise serializers.ValidationError({"detail":"Invalid amount"})
    return value

class DepositSerializer(serializers.Serializer) :

    amount = serializers.IntegerField(validators=[is_amount])
    email = serializers.EmailField()

    def validate_email(self,attrs) :
        if User.objects.filter(email=attrs).exists():
            return attrs
        raise serializers.ValidationError({"details":"Email not found"})

    def save(self) :
        user = self.context['request'].user
        wallet = Wallet.objects.filter(user=user).exists()
        if not wallet:
            wallet = Wallet.objects.create(user=user)
        wallet = Wallet.objects.get(user=user)
        data = self.validated_data
        url = "https://api.paystack.co/transaction/initialize"
       
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.post(url, headers = headers, data=data)
        response = r.json()
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type ='deposits',
            amount = data["amount"],
            paystack_payment_ref= response['data']['reference'],status="pending"
        )

        return response
