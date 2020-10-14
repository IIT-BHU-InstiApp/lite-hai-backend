from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from fcm_django.models import FCMDevice
from workshop.permissions import AllowAnyClubHead
from .models import UserProfile
from .serializers import (
    LoginSerializer, ProfileSerializer, ResponseSerializer, ProfileSearchSerializer)

def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    # pylint: disable=no-member
    token, _ = Token.objects.get_or_create(user=user)
    return token


def send_notification(message, title):
    """
    Send notification to all users using Firebase Cloud Messaging
    """
    devices = FCMDevice.objects.all()
    devices.send_message(title=title, body=message)
    return True

class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks the credentials (taking firebase **idToken** as input)\
        and returns the **REST Token** (Authentication Token),\
        if the credentials are valid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = create_auth_token(user)
        response = ResponseSerializer({'token': token})
        return Response(response.data, status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    get:
    Returns the Name, Email, Phone Number, Department, Year of Joining\
    and Photo URL of the user. Also returns the subscriptions and\
    club privileges of the user.

    put:
    Updates the name, phone_number and photo of User Profile and\
    returns all the fields. (Full update)

    patch:
    Updates the name, phone_number and photo of User Profile and\
    returns all the fields. (Partial update)
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        # pylint: disable=no-member
        return UserProfile.objects.get(user=self.request.user)


class ProfileSearchView(generics.GenericAPIView):
    permission_classes = (AllowAnyClubHead, )
    serializer_class = ProfileSearchSerializer

    def post(self, request):
        """
        Search a user based on Name or Email. (Only Top 10 results)
        Only Club POR holders can perform this action.
        (Can be used to search profile while adding contacts for a workshop)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        response = ProfileSerializer(profile, many=True)
        return Response(response.data, status.HTTP_200_OK)
