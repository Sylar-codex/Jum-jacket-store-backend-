from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import Util

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ('id','username','email','first_name','last_name',)

class RegisterSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ('id','first_name', 'last_name','email','password','username')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data) :
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])
        return user

class LoginSerializers(serializers.Serializer) :
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data) :
        user = authenticate(**data)
        if user and user.is_active :
            return user 
        raise serializers.ValidationError("incorrect credentials")

class ResetPasswordEmailRequestSerializer(serializers.Serializer) :
    email = serializers.EmailField()
    
    class Meta :
        fields =['email']

class SetNewPasswordSerializer(serializers.Serializer) :
    password = serializers.CharField(min_length=6,write_only=True)
    token = serializers.CharField(min_length=6,write_only=True )
    uidb64 = serializers.CharField(min_length=1,write_only=True)

    class Meta:
        fields= ["password","token","uidb64"]
    def validate(self, data):
        password = data.get('password')
        token = data.get('token')
        uidb64 = data.get('uidb64')
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("The reset link is invalid")
        user.set_password(password)
        user.save()
        return user 
        
