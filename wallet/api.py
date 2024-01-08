from rest_framework import generics, permissions
from .serializers import WalletSerializer, DepositSerializer
from .models import Wallet, WalletTransaction
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework import viewsets, permissions
from knox.auth import TokenAuthentication
from django.conf import settings
import requests
import json


class WalletInfoAPI(generics.GenericAPIView) :
    authentication_classes =(TokenAuthentication,)
    permission_classes = {
        permissions.IsAuthenticated
    }
    serializer_class = WalletSerializer
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        data = self.get_serializer(wallet).data
        return Response (data)

class DepositFundsAPI(generics.GenericAPIView) :
    authentication_classes =(TokenAuthentication,)
    permission_classes = {
        permissions.IsAuthenticated
    }
    serializer_class = DepositSerializer
    def post(self,request) :
        serializer = self.get_serializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception= True)
        resp = serializer.save()
        return Response(resp)

class VerifyDepositAPI(generics.GenericAPIView) :
    authentication_classes =(TokenAuthentication,)
    permission_classes = {
        permissions.IsAuthenticated
    }
    def get(self,request,reference) :
        transaction=WalletTransaction.objects.get(paystack_payment_ref=reference, wallet__user=request.user)
        reference= transaction.paystack_payment_ref
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        
        headers ={"authorization":f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        r = requests.get(url, headers=headers)
        resp = r.json()

        if resp['data']['status'] == 'success' :
            status = resp['data']['status']
            amount = resp['data']['amount']
            WalletTransaction.objects.filter(paystack_payment_ref=reference).update(status=status, amount=amount)

            return Response(resp)
        return Response(resp)

class PaystackWebhookView(generics.GenericAPIView) :
    def post(self,request,*args,**kwargs) :
        data = json.loads(request.body.decode("utf-8"))
        return Response(data={})
