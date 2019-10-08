from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def create_auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


class RegisterView(generics.GenericAPIView):
    authentication_classes=[]
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self,request):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)  
        self.user = self.serializer.save()
        self.token = create_auth_token(self.user)
        response = ResponseSerializer({'message':self.token})
        return Response(response.data,status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self,request):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.user = self.serializer.validated_data['user']
        self.token = create_auth_token(self.user)
        response = ResponseSerializer({'message':self.token})
        return Response(response.data,status.HTTP_200_OK)


