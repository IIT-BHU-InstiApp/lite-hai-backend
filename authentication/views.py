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


class LoginView(generics.GenericAPIView):
    """
    Checks the credentials and returns the REST Token (Authentication Token) if the credentials are valid.
    """
    authentication_classes = []
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self,request):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.user = self.serializer.validated_data['user']
        self.token = create_auth_token(self.user)
        response = ResponseSerializer({'token': self.token})
        return Response(response.data, status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    <b>GET</b>: Returns the Name, Email, Department and Year of Joining of the user.
    <b>PUT/PATCH</b>: Updates the name of User Profile and returns the Name, Email, Department and Year of Joining.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)