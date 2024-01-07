import os
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer,LoginSerializers,RegisterSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import render


#Register API
class RegisterAPI(generics.GenericAPIView) :
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user':UserSerializer(user, context = self.get_serializer()).data,
            'token':AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView) :
    serializer_class = LoginSerializers
    def post(self, request,*args, **kwargs) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            'user':UserSerializer(user, context=self.get_serializer()).data,
            'token':AuthToken.objects.create(user)[1]
        })

class UserAPI(generics.RetrieveAPIView) :
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class RequestPasswordResetEmail(generics.GenericAPIView) :
    serializer_class = ResetPasswordEmailRequestSerializer
    
    def post(self,request) :
        serializer = self.get_serializer(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists() :
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            # relativeLink = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,"token":token})
            # absurl = 'http://'+ current_site + relativeLink
            frontend_host = os.environ.get("FRONTEND_HOST")
            email_body = "https://{}/#/reset-password/{}/{}".format(frontend_host,uidb64,token)
            email_data = {'email_body':email_body, "to_email":user.email,"email_subject":"reset your password"}

            Util.send_email(email_data)

        return Response({"succes":True,"message":"A link has been sent to your email to reset your password, check spam folder as well"})

class PasswordTokenCheckAPI(generics.GenericAPIView) :
    serializer_class = SetNewPasswordSerializer
    def get(self,request,uidb64,token):
        try: 
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
           
            # check if a user has used the token before
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({"error":"Token is invalid"})
            return Response({"success":True,"message":"credentails valid","uidb64":uidb64,"token":token})
           
        except DjangoUnicodeDecodeError as identifier :
                return Response({"error":"Token is invalid"})

class SetNewPasswordAPI(generics.GenericAPIView) :
    serializer_class = SetNewPasswordSerializer

    def patch(self,request,):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success":True,"message":"You have successfully reset your password"})
