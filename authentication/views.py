from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import LoginSerializer, ProfileSerializer, ResponseSerializer

def create_auth_token(user):
    """
    Returns the token required for authentication for a user
    """
    # pylint: disable=no-member
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    """
    Checks the credentials and returns the REST Token (Authentication Token)
    if the credentials are valid.
    """
    authentication_classes = []
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles the POST request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = create_auth_token(user)
        response = ResponseSerializer({'token': token})
        return Response(response.data, status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    <b>GET</b>: Returns the Name, Email, Department and Year of Joining of the user.
    <b>PUT/PATCH</b>: Updates the name of User Profile and returns the Name, Email,
    Department and Year of Joining.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        # pylint: disable=no-member
        return UserProfile.objects.get(user=self.request.user)
